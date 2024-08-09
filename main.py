from operator import itemgetter

from langchain.chains import create_sql_query_chain
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough, chain
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine

from api import logger
from chains import *

db_user = "root"
db_password = "anas123"
db_host = "localhost:3306"
db_name = "acr"


def local():
    engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")
    return engine


def remote():
    engine = create_engine(
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
    )
    return engine


_db = None


def connect_db():
    global _db

    def connect():

        engine = local()
        _db = SQLDatabase(engine=engine)
        _db._sample_rows_in_table_info = 0
        return _db

    if not _db:
        logger.info("Connecting to database")
        _db = connect()
        logger.info("Connected to database")
    else:
        try:
            _db.run("SELECT 1")  # just to check whether the connection is active or not
        except Exception as e:
            logger.info("SQL {}", str(e))
            logger.info("Reconnecting to database")
            _db = connect()
            logger.info("Reconnected to database")
    return _db


llm = ChatOpenAI(model="gpt-4o", temperature=0)

system = """You are a MySQL expert. Given an input question, create a syntactically
correct MySQL INSERT/UPDATE query to run and always give a proper column names while using aggregation.
- If the sentence is Interrogative Sentences then only generate SELECT query
- If the input has add generate INSERT
- NEVER EVER  insert any values not given in input
- If the input has update generate UPDATE
- If prompted to fetch entire information from multiple tables, avoid using UNION ALL operations. Instead, use multiple separate SELECT queries for each table.
Unless otherwise specified, do not return more than
{top_k} rows.
Only return the SQL query with no markup or explanation.
Here is the relevant table info only refer the CREATE but DO NOT REFER THE EXAMPLE ROWS GIVEN: {table_info}
"""
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{input}")])


memory_patient_info = ConversationBufferMemory()

# Define the prompt template for answering
rephrase_prompt = ChatPromptTemplate.from_template(
    """Given the following user query and conversation log,if the conversation log does not have a prior history keep the query as it is. Else formulate a new question which has all the details mentioned in the prior conversations
   If the current query is asking to proceed then provide me the last Query according to the logs and only return Refined Query

   CONVERSATION LOG: {rephrase_conversation}
   Query: {question}
   Refined Query : """
)

rephrase_chain = (
    rephrase_prompt | llm | StrOutputParser() | RunnablePassthrough(logger.debug)
)


insert_chain = RunnablePassthrough() | validate_insert_query_chain

update_chain = RunnablePassthrough() | validate_update_query_chain


@chain
def validate(result: Dict[str, str]) -> Dict[str, str]:
    logger.debug(result["queries"])
    if "INSERT INTO" in result["query"]:
        return insert_chain
    elif "UPDATE" in result["query"]:
        return update_chain
    else:
        memory_patient_info.clear()
        return {**result, "message": "Only for insert or update", "is_proceed": True}


@chain
def generate_query(data):
    generate_query_insert = create_sql_query_chain(llm, data["db"], prompt=prompt)
    data["query"] = generate_query_insert.invoke({"question": data["question"]})
    return data

data_manipulation_chain = (
    update_qn
    | RunnablePassthrough()
    .assign(old_question=itemgetter("question"))
    .assign(conversation=itemgetter("memory") | get_conversation)
    .assign(
        rephrase_conversation=itemgetter("conversation") | get_rephrase_conversation
    )
    .assign(question=rephrase_chain)
    | generate_query
    | RunnablePassthrough()
    .assign(queries=itemgetter("query") | get_queries)
    .assign(is_proceed=itemgetter("old_question") | can_we_proceed)
    | validate
    #pending_side
    | evaluate_result
    | update_history
)


# @chain
# def execute_query(data):
#     _query = data["query"].split(";")
#     print("this->",_query, "<-This")
#     result_=[]
#     for i in _query:
#         i = i.strip("\n") + ";"
#         if len(i) < 10:
#             continue
#         print("-> ", i, " <-")
#         result_.append(data["db"].run_no_throw(i, include_columns=True))
#         print("This is the result",result_)
#     return result_


@chain
def execute_query(data):
    query= data["query"]
    extracted_queries = [q.replace("\n", " ").strip() for q in query.split(";")]
    print("this->",extracted_queries, "<-This")
    result_=[]
    for i in extracted_queries:
        i = i.strip("\n") + ";"
        if len(i) < 10:
            continue
        print("-> ", i, " <-")
        result_.append(data["db"].run_no_throw(i, include_columns=True))
        print("This is the result",result_)
    return result_




    # extracted_queries = [q.replace("\n", " ").strip() for q in query.split(";")]
    # extracted_queries = [q for q in extracted_queries if q != ""]
    # return extracted_queries


# Define the answer prompt template
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, conversation, corresponding SQL query, and SQL result, answer the user question with explanation of the result.
    Conversation so far: {conversation}
    Question: {question}
    SQL Query: {query}
    if SQL Query throw an error, Say "Unable to fetch the details, please try once again"
    SQL Result: {result}

    Answer:
    If the SQL Result is empty just say There are no records for that value in a natural language.
    and prohibit using the following 'sql',query','based on', 'data base'
    also talk like a normal person and never use Markup"""
)

# Define the rephrase answer sequence
rephrase_answer = answer_prompt | llm | StrOutputParser()


# def reconnect_db():
#     global db
#     engine = remote()
#     db = SQLDatabase(engine=engine)
#     db._sample_rows_in_table_info = 0


### Retrieval
@chain
def update_history_retrieval(result):
    mem: ConversationBufferMemory = result["memory"]
    mem.save_context({"input": result["question"]}, {"output": result["message"]})
    return result


@chain
def log(result):
    logger.debug("Question : {}", result["question"])
    logger.debug("Query : {}", result["query"])
    logger.debug("Result : {}", result["result"])
    return result


retrieval_rephrase_prompt = ChatPromptTemplate.from_messages(
    (
        "system",
        "Given the following user query and conversation log,if the conversation log does not have a prior history keep the query as it is. Else formulate the most relevant question to provide the user with an answer from data base if the result is 1/0 consider it as boolean \n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {question}\n\nRefined Query:",
    )
)
data_retrieval_chain = (
    RunnablePassthrough()
    .assign(conversation=itemgetter("memory") | get_conversation)
    .assign(question=retrieval_rephrase_prompt | llm | StrOutputParser())
    | generate_query
    | RunnablePassthrough().assign(result=execute_query).assign(message=rephrase_answer)
    | log
    | update_history_retrieval
)