import re

import numpy as np
from langchain_openai import OpenAIEmbeddings


def get_embedding(sentence: str):
    return OpenAIEmbeddings().embed_query(sentence)


from typing import Dict, List, Literal


def igetattr(obj, attr):
    val = None
    for a in dir(obj):
        if a.lower() == attr.lower():
            val= getattr(obj, a)
            return getattr(obj, a)
        
    if val is None:
        return getattr(obj, attr)



def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def dictionary_to_query(
    provided_fields: List[Dict[str, str | Dict[str, str]]],
    table_name,
    mode: Literal["i", "u"],
):
    column_names = [
        k for k in provided_fields[0].keys() if k != "table_name_for_reference"
    ]
    sql_functions = ["CURDATE", "NOW"]

    def gen_column_values(v: str) -> str:
        v = str(v)
        new_values = f"'{v}'"
        for f in sql_functions:
            if f in v.upper():
                new_values = v.replace(f, f + "()")
        return new_values

    def gen_update_values(values: Dict[str, str]) -> str:
        return ", ".join(
            [
                f"{k} = {gen_column_values(v)}"
                for k, v in values.items()
                if k != "table_name_for_reference"
            ]
        )

    def gen_insert_values(values: Dict[str, str]) -> str:
        return ",".join(
            gen_column_values(v)
            for k, v in values.items()
            if k != "table_name_for_reference"
        )

    if mode == "i":
        query = f"""INSERT INTO {table_name} ({', '.join(column_names)}) VALUES {",".join([f"({gen_insert_values(values)})" for values in provided_fields])}"""
    elif mode == "u":
        values = provided_fields[0]
        set_values = values["set"]
        where = values.get("where", {})
        query = f"""UPDATE {table_name} SET {gen_update_values(set_values)} WHERE {gen_update_values(where)}"""
    else:
        raise ValueError("mode can be i or u in dictionary_to_query function ")
    return query


pytypes = {
    "integer": "int",
    "int": "int",
    "text": "str",
    "date": "str",
    r"enum\((?P<enum_vals>.*)\)": "enum",
    r"tinyint\([\d]+\)": "int",
    r"varchar\([\d]+\)": "str",
    "time": "str",
}


def get_type(t: str) -> str:
    t = t.strip(",")
    for k, v in pytypes.items():
        m = re.match(k, t, re.IGNORECASE)
        if m:
            if v == "enum":
                enum_vals = m.group("enum_vals").split(",")
                return v, enum_vals
            return v, []
    print(f"Unknown type {t}")
    return "str", []


def sql_to_pydantic(test_str):

    table_regex = re.compile(
        r"CREATE\s+TABLE\s+`(?P<table_name>[^\s]*)`\s+\((?P<content>.*?)PRIMARY",
        re.DOTALL,
    )
    regex = r"\s*`*(?P<column_name>[^\s,]+)`*\s*(?P<type>[^\s]+)[\(\)\s,\d]*(?:DEFAULT\s+(?P<default_value>[^\s,]+))?(?P<not_null>NOT\s+NULL)?(?P<auto_increment>\s+AUTO_INCREMENT)?"
    class_body_template = """class {class_name}(BaseModel):\n{columns}\n\n"""

    column_template = """\t{column_name}:{type} {default_value}"""
    enum_body_template = "class {class_name}(str,Enum):\n{enum_body}\n\n"
    enum_value_template = "\t{enum_value} = '{enum_value}'"
    tables = [x.groupdict() for x in re.finditer(table_regex, test_str)]
    class_codes = ["from pydantic import BaseModel", "from enum import Enum"]
    for table in tables:
        table_name = table["table_name"]
        content = ", " + table["content"]
        # print(content)
        # table_name = re.search(r"CREATE\s*TABLE\s*`(?P<table_name>.*)`",content).groupdict()['table_name']
        matches = re.finditer(regex, content, re.MULTILINE)
        columns = []
        for match in matches:
            # print(match.groupdict())
            columns.append(match.groupdict())

        defaults = {"NULL": "''"}
        class_code = f"""class {table_name}(BaseModel):\n"""
        enum_body = []
        py_columns = []
        for column in columns:
            if column["column_name"] == "":
                continue
            if column["type"] == "":
                continue
            column["column_name"] = column["column_name"].strip("`")

            t, enum_vals = get_type(column["type"])
            default_value = ""
            if len(enum_vals) > 0:
                t = column["column_name"] + "Enum"
                enum_body.append(
                    enum_body_template.format(
                        class_name=column["column_name"] + "Enum",
                        enum_body="\n".join(
                            [
                                enum_value_template.format(enum_value=x.strip("'"))
                                for x in enum_vals
                            ]
                        ),
                    )
                )

            if column["auto_increment"]:
                column["default_value"] = "'0'"
            if column["default_value"]:
                default_value = " = {}".format(
                    defaults.get(
                        column["default_value"],
                        (
                            column["default_value"].strip("'")
                            if t == "int"
                            else column["default_value"]
                        ),
                    )
                )
            py_columns.append(
                column_template.format(
                    column_name=column["column_name"],
                    type=t,
                    default_value=default_value,
                )
            )
        class_code = "\n".join(enum_body) + class_body_template.format(
            class_name=table_name + "_INSERT", columns="\n".join(py_columns)
        )
        class_codes.append(class_code)
        py_columns = []
        for column in columns:
            if column["column_name"] == "":
                continue
            if column["type"] == "":
                continue
            column["column_name"] = column["column_name"].strip("`")

            t, enum_vals = get_type(column["type"])
            default_value = ""
            if len(enum_vals) > 0:
                t = column["column_name"] + "Enum"

            if column["auto_increment"]:
                column["default_value"] = "'0'"

            default_value = " = {}".format(
                defaults.get(
                    column["default_value"],
                    (
                        column["default_value"].strip("'")
                        if t == "int"
                        else column["default_value"]
                    ),
                )
                if column["default_value"]
                else "0" if t == "int" else "''"
            )
            py_columns.append(
                column_template.format(
                    column_name=column["column_name"],
                    type=t,
                    default_value=default_value,
                )
            )
        class_code = class_body_template.format(
            class_name=table_name + "_UPDATE", columns="\n".join(py_columns)
        )
        class_codes.append(class_code)

    return "\n".join(class_codes)
