import importlib
from typing import Any, Dict, List, Tuple, Union

import numpy as np
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import chain
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError
from sqlalchemy import text

# from validators import CaseInsensitiveAdapter


from api import logger
from utils import cosine_similarity, dictionary_to_query, get_embedding, igetattr

llm = ChatOpenAI(model="gpt-4o", temperature=0)


@chain
def get_validator_class_for_update(table_name: str) -> BaseModel:
    if table_name.lower() == "patientinfo":
        table_name = "PatientDetailsUpdate"

    return get_validator_class_for_insert.invoke(table_name)


@chain
def get_validator_class_for_insert(table_name: str) -> BaseModel:
    if table_name.split("_")[0].lower() == "case" or "medical":
        if not table_name.split("_")[-1].lower() == "insert":
            table_name = table_name + "_insert"

    if table_name.lower() == "patientinfo":
        print(f"\n\ntable name changed from {table_name} to PatientDetailsInsert\n\n")
        table_name = "PatientDetailsInsert"

    module = importlib.import_module(f"validators")
    return igetattr(module, table_name)


@chain
def extract_table_name_from_insert(query: str) -> str:
    # Extract the table name from the query
    # word after INTO keyword
    return query.split()[query.split().index("INTO") + 1].strip().replace("`", "")


@chain
def extract_table_name_from_update(query: str) -> str:
    # Extract the table name from the query
    # word after INTO keyword
    return query.split()[query.split().index("UPDATE") + 1].strip().replace("`", "")


@chain
def evaluate_result(result: Dict[str, Any]) -> Dict[str, Any]:
    missing_fields = result["missing_fields"]
    provided_fields = result["provided_fields"]
    conversation = result["conversation"]
    db = result["db"]
    if len(missing_fields) > 0:
        message = "These are the errors found in the given data \n - "
        message += "\n - ".join([f"{x['field']} = {x['type']}" for x in missing_fields])
        field_error_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "This is the conversation so far {conversation} and based on the details provided so far we have found these errors {errors} now u have to ask the users to enter these details for example 'May I get <fields> details ' ",
                )
            ]
        )
        field_error_chain = field_error_prompt | llm | StrOutputParser()
        message = field_error_chain.invoke(
            {"errors": missing_fields, "conversation": result["conversation"]}
        )
    else:
        if result["is_proceed"]:
            try:
                filtered_queries = result["filtered_queries"]
                with db._engine.begin() as conn:
                    for q in filtered_queries:
                        conn.execute(text(q + ";"))
                result["memory"].clear()
                success_prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", "This is the conversation so for {conversation}"),
                        (
                            "system",
                            "You have successfully ran the query : {query} Now you have to tell the user with a nice message that these changes have been successfully completed ONLY return the message  ",
                        ),
                    ]
                )
                success_chain = success_prompt | llm | StrOutputParser()
                message = success_chain.invoke(
                    {"query": result["query"], "conversation": conversation}
                )

            except Exception as e:
                logger.error(str(e))
                error_prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            """You were trying to run a query and got the error {error}
                                Now tell the user what issue you had and ask the user to enter the proper data 
                               For Example :
                                    Foreign key error patient id 3 does not exist 
                                    your response would be Patient with id 3 does not exist please check it once

                               """,
                        ),
                        (
                            "human",
                            "Give me a nice message I could show it to the user adn ask to enter the correct data ",
                        ),
                    ]
                )
                error_chain = error_prompt | llm | StrOutputParser()
                message = error_chain.invoke(
                    {
                        "error": str(e),
                    }
                )
        else:

            proceed_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "This is the conversation so far {conversation}"),
                    (
                        "system",
                        """You are interacting with a user and user have given the following data  , I want you to talk to user and tell him that these are the values you entered 
                         Is this all right and do you want to proceed and if the data contains SQL date/time function then translate them into regular english like today,tomorrow etc""",
                    ),
                    ("human", "{message}"),
                ]
            )
            proceed_chain = proceed_prompt | llm | StrOutputParser()
            message = proceed_chain.invoke(
                {"message": provided_fields, "conversation": conversation}
            )

    result["message"] = message
    return result


@chain
def update_history(results: Dict[str, Any]) -> Dict[str, Any]:
    memory = results["memory"]
    if not results["is_proceed"]:
        memory.save_context({"input": results["question"]}, {"outputs": ""})
    return results


# Example sentences
positive_examples = ["please proceed with the task.", "yes", "yes proceed"]

negative_examples = ["do not proceed with this.", "no", "do not proceed"]

# Compute embeddings for example sentences
positive_embeddings = [get_embedding(sentence) for sentence in positive_examples]
negative_embeddings = [get_embedding(sentence) for sentence in negative_examples]


@chain
def can_we_proceed(sentence: str) -> bool:
    sentence = sentence.split(":")[-1]
    sentence = sentence.lower()
    sentence_embedding = get_embedding(sentence)

    # Calculate average similarity to positive and negative examples
    positive_similarity = np.mean(
        [
            cosine_similarity(sentence_embedding, pos_embed)
            for pos_embed in positive_embeddings
        ]
    )
    negative_similarity = np.mean(
        [
            cosine_similarity(sentence_embedding, neg_embed)
            for neg_embed in negative_embeddings
        ]
    )

    return positive_similarity > negative_similarity and positive_similarity > 0.8


@chain
def validate_insert_query_chain(
        result: Dict[str, Union[str, BaseModel]]
) -> Dict[str, Union[List[Dict[str, str]], List[Dict[str, str]]]]:
    """
    Validate the insert query and return the missing fields and provided fields.

    Args:
        result (Dict[str, Union[str, Type[BaseModel]]]): A dictionary containing the query
            and the validator class.

    Returns:
        Dict[str, Union[List[Dict[str, str]], List[Dict[str, str]]]]: A dictionary containing
            the missing fields and provided fields.
    """
    invalid_values = ["", "NULL", "0000-00-0", "None", "NONE"]

    def split_columns_values(s):
        items = []
        current = []
        parens = 0
        in_quotes = False
        for char in s:
            if char == "," and parens == 0 and not in_quotes:
                items.append("".join(current).strip())
                current = []
            else:
                if char == " " and len(current) == 0:
                    continue
                if char == "(":
                    parens += 1
                elif char == ")":
                    parens -= 1
                elif char in ["'", '"'] and (len(current) == 0 or current[-1] != "\\"):
                    in_quotes = not in_quotes
                current.append(char)
        items.append("".join(current).strip())
        items = [item.strip("'") for item in items]
        return items

    def validate_query(
            query: str, cls: BaseModel
    ) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        query = query.replace("()", " ")
        _a = query[query.find("(") + 1: query.find(")")]
        # split the data using ,
        _b = _a.split(",")
        # extract column names
        columns = [i.strip().strip("`").strip('"').strip("'") for i in _b]
        # if column name starts with '," or ` then remove it

        values_query = query.split("VALUES")[1].strip()

        # Find all sets of values in the VALUES part
        values_sets = values_query.split("), (")

        # Clean and split each set of values
        cleaned_values_sets = []
        for values_set in values_sets:
            # values_set = values_set[values_set.find("(") + 1 : values_set.find(")")]
            # _b = values_set.split(",")
            # values = [i.strip().strip("`").strip("'") for i in _b]
            values_set = values_set.strip("(").strip(")")
            print(values_set)
            values = split_columns_values(values_set)
            cleaned_values_sets.append(values)

        # Create a list of dictionaries, one for each set of values
        values_dicts = []
        for values in cleaned_values_sets:
            values_dict = {c: v for c, v in zip(columns, values)}
            # Remove entries whose value is ''
            values_dict = {
                k: v for k, v in values_dict.items() if v not in invalid_values
            }
            values_dicts.append(values_dict)
        logger.debug(values_dict)
        missing_fields = []
        provided_fields = []
        try:
            print("all value is \n", values_dicts)
            for values_dict in values_dicts:

                print("\n------\n", values_dict, "\n-----\n")

                medical_history_implant_classes = ["medical_history_Implants", "medical_history_Implants_INSERT",
                                                   "medical_history_Implants_UPDATE"]

                if cls.__name__ in medical_history_implant_classes and (
                        "implant_name" not in values_dict
                        or values_dict["implant_name"] in invalid_values
                ):
                    logger.info(
                        f"Dropped values of table {cls.__name__} values = {values_dict}"
                    )
                    continue
                # adapter= CaseInsensitiveAdapter(cls)
                # _ = adapter.validate_python(values_dict)
                print("each one is :\n", values_dict)

                _ = cls(**values_dict)

                _insert_update_names = ["insert", "update"]

                if str(cls.__name__).split('_')[-1].lower() in _insert_update_names:

                    parts = str(cls.__name__).split("_")
                    referance = "_".join(parts[:-1])
                    values_dict["table_name_for_reference"] = referance
                    # values_dict["table_name_for_reference"] = str(cls.__name__).split("_")[-2]

                else:
                    # values_dict["table_name_for_reference"] = str(cls.__name__).split("_")[-1]
                    values_dict["table_name_for_reference"] = str(cls.__name__)

                provided_fields.append(values_dict)
        except ValidationError as e:
            errors = e.errors()
            # logger.debug(errors)
            missing_fields = [
                {
                    "field": x["loc"][0],
                    "type": x["msg"],
                    "tablename_for_hint": str(cls.__name__).split("_")[-1],
                }
                for x in errors
            ]
        return missing_fields, provided_fields

    missing_fields = []
    provided_fields = []
    filtered_queries = []
    print("\n\n", result["queries"], "\n\n")
    for query in result["queries"]:
        if len(query) < 10:
            continue
        print(f"\n\n1 from above of extract_table_name_from_insert: {query}\n\n")
        table_name = extract_table_name_from_insert.invoke(query)
        print(f"tabel name is {table_name}")
        print(f"\n\n2 from below of extract_table_name_from_insert: {query}\n\n")
        m_fields, p_fields = validate_query(
            query,
            get_validator_class_for_insert.invoke(table_name),
        )

        logger.debug("Provided Fields = {}", p_fields)
        logger.debug("Missing Fields {}", m_fields)
        missing_fields.extend(m_fields)
        if len(p_fields) > 0:
            provided_fields.extend(p_fields)
            filtered_queries.append(dictionary_to_query(p_fields, table_name, mode="i"))
    result["missing_fields"] = missing_fields
    result["provided_fields"] = provided_fields
    result["filtered_queries"] = filtered_queries
    return result


@chain
def validate_update_query_chain(
        result: Dict[str, Union[str, Any]]
) -> Dict[str, Union[List[Dict[str, str]], List[Dict[str, str]]]]:
    """
    Validate the update query and return the missing fields and provided fields.

    Args:
        result (Dict[str, Union[str, Type]]): The result dictionary containing the query and validator class.

    Returns:
        Dict[str, Union[List[Dict[str, str]], List[Dict[str, str]]]]: The result dictionary with missing fields and provided fields.
    """

    def validate_query(
            query: str, cls: BaseModel
    ) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """
        Validate the update query and return the missing fields and provided fields.

        Args:
            query (str): The update query.
            cls (Type): The validator class.

        Returns:
            Tuple[List[Dict[str, str]], List[Dict[str, str]]]: The missing fields and provided fields.
        """
        query = query.replace("\n", " ")
        query = query.replace("()", " ")
        # UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition;
        if "WHERE" in query:
            _a = query[query.index("SET") + 3: query.index("WHERE")]
        else:
            _a = query[query.index("SET") + 3:]
        values_dict = {
            cv.split("=")[0]
            .strip()
            .strip("`")
            .strip("'"): cv.split("=")[1]
            .strip()
            .strip("`")
            .strip("'")
            for cv in _a.split(",")
        }
        where_values_dict = dict()
        if "WHERE" in query:
            # extract those fields
            _a = query.split("WHERE")[1]
            _a = _a.replace(";", "")
            where_values_dict = {
                cv.split("=")[0]
                .strip()
                .strip("`")
                .strip("'"): cv.split("=")[1]
                .strip()
                .strip("`")
                .strip("'")
                for cv in _a.split(",")
            }
        set_values = values_dict
        values_dict = {**values_dict, **where_values_dict}
        logger.debug(values_dict)
        missing_fields = []
        try:
            _ = cls(**values_dict)
        except ValidationError as e:
            errors = e.errors()
            # logger.debug(errors)
            missing_fields = [{"field": x["loc"][0], "type": x["msg"]} for x in errors]
        return missing_fields, [{"set": set_values, "where": where_values_dict}]

    missing_fields = []
    provided_fields = []
    for query in result["queries"]:

        if len(query) < 10:
            continue

        m_fields, p_fields = validate_query(
            query,
            get_validator_class_for_update.invoke(
                extract_table_name_from_update.invoke(query)
            ),
        )
        logger.debug("Provided Fields = {}", p_fields)
        logger.debug("Missing Fields {}", m_fields)

        missing_fields.extend(m_fields)
        provided_fields.extend(p_fields)

    result["missing_fields"] = missing_fields
    result["provided_fields"] = provided_fields
    result["filtered_queries"] = result["queries"]
    return result


@chain
def get_conversation(memory: ConversationBufferMemory):
    return memory.load_memory_variables({}).get(
        "history", "No prior conversation history."
    )


@chain
def update_qn(a):
    a["question"] = "and " + a["question"]
    return a


@chain
def get_queries(query):
    extracted_queries = [q.replace("\n", " ").strip() for q in query.split(";")]
    extracted_queries = [q for q in extracted_queries if q != ""]
    print("\n From get_queries\n", extracted_queries, "\n----\n")
    return extracted_queries


@chain
def get_rephrase_conversation(conversation: str):
    return "\n".join(m for m in conversation.split("\n") if m.startswith("Human"))