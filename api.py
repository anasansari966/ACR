import os
import re

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from memory_buffers import *
from utils import sql_to_pydantic

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# do not move this line , API_KEY is required in main.py
from main import *

logger.add("ACR_DEBUG_LOG.log", rotation="500 MB", enqueue=True)

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


clear_history_regex = r".*clear memory$"


@app.get("/select/medical_history")
def get_medical_history(question: str):
    db = connect_db()
    if re.match(clear_history_regex, question.lower()) is not None:
        memory_select.clear()
        return "Memory Cleared"
    # try:
    result = data_retrieval_chain.invoke(
        {
            "question": question,
            "db": db,
            "memory": memory_select,
            "table_names_to_use": [
                "medical_history_Autonomic",
                "medical_history_CoMorbidities",
                "medical_history_Diagnosis",
                "medical_history_Implants",
                "medical_history_MotorFunction",
                "medical_history_Note",
                "medical_history_Seizures",
                "medical_history_Surgeries",
                "medical_history_Symptoms",
                "PatientInfo",
                "PatientInfo_extension",
            ],
        }
    )
    # except Exception as e:
    #     logger.debug(str(e))
    #     logger.info("Reconnecting DB")
    #     # reconnect_db()
    #     result = dict()
    #     result["message"] = "Something went wrong please retry..."
    return result["message"]


@app.get("/select/case_study")
def insert_patient(question: str):
    db = connect_db()
    if re.match(clear_history_regex, question.lower()) is not None:
        memory_case_study_retrieval.clear()
        return "Memory Cleared"
    try:
        result = data_retrieval_chain.invoke(
            {
                "question": question,
                "memory": memory_case_study_retrieval,
                "db": db,
                "table_names_to_use": [
                    "Case_setup_CranialMuscles",
                    "Case_setup_EEG_channels",
                    "Case_setup_EMG_Muscles",
                    "Case_setup_MEP_Muscles",
                    "Case_setup_Modalties",
                    "Case_setup_SSEP",
                    "Case_setup_SSEP_Nerves",
                    "Case_setup_mep",
                    "Case_setup_trig_emg",
                ],
            }
        )
    except Exception as e:
        logger.debug(str(e))
        logger.info("Reconnecting DB")
        # reconnect_db()
        result = dict()
        result["message"] = "Something went wrong please retry..."
    return result["message"]


@app.get("/insert/medical_history")
def insert_medical_history(question: str):
    db = connect_db()
    if re.match(clear_history_regex, question.lower()) is not None:
        memory_patient_info.clear()
        return "Memory Cleared"
    try:
        result = data_manipulation_chain.invoke(
            {
                "question": question,
                "memory": memory_medical_history,
                "db": db,
                "table_names_to_use": [
                    "medical_history_Autonomic",
                    "medical_history_CoMorbidities",
                    "medical_history_Diagnosis",
                    "medical_history_Implants",
                    "medical_history_MotorFunction",
                    "medical_history_Note",
                    "medical_history_Seizures",
                    "medical_history_Surgeries",
                    "medical_history_Symptoms",
                ],
            }
        )
        # result["message"] = "Production still in progress, please dont test here"
    except Exception as e:
        logger.debug(str(e))
        logger.info("Reconnecting DB")
        # reconnect_db()
        result = dict()
        result["message"] = "Something went wrong please retry..."
    return result["message"]


@app.get("/insert/patient")
def insert_patient(question: str):
    db = connect_db()
    # if question.lower() == "clear memory":
    if re.match(clear_history_regex, question.lower()) is not None:
        memory_patient_info.clear()
        return "Memory Cleared"
    try:
        result = data_manipulation_chain.invoke(
            {
                "question": question,
                "db": db,
                "memory": memory_patient_info,
                "table_names_to_use": [
                    "PatientInfo",
                    "PatientInfo_extension",
                ],
            }
        )
        # result["message"] = "Production still in progress, please dont test here"
    except Exception as e:
        logger.debug(str(e))
        logger.info("Reconnecting DB")
        # reconnect_db()
        result = dict()
        result["message"] = "Something went wrong please retry..."
    return result["message"]


@app.get("/insert/case_study")
def insert_patient(question: str):
    db = connect_db()
    if re.match(clear_history_regex, question.lower()) is not None:
        memory_case_study.clear()
        return "Memory Cleared"
    try:
        result = data_manipulation_chain.invoke(
            {
                "question": question,
                "db": db,
                "memory": memory_case_study,
                "table_names_to_use": [
                    'Case_setup_CranialMuscles',
                    'Case_setup_EEG_channels',
                    'Case_setup_EMG_Muscles',
                    'Case_setup_MEP_Muscles',
                    'Case_setup_Modalties',
                    'Case_setup_SSEP',
                    'Case_setup_SSEP_Nerves',
                    'Case_setup_mep',
                    'Case_setup_trig_emg'],
            }
        )
        # result["message"] = "Production still in progress, please dont test here"
    except Exception as e:
        logger.debug(str(e))
        logger.info("Reconnecting DB")
        # reconnect_db()
        result = dict()
        result["message"] = "Something went wrong please retry..."
    return result["message"]


@app.get("/patient")
def get_patients():
    db = connect_db()
    try:
        cursor = db.run(
            "Select patient_id,FirstName from PatientInfo",
            include_columns=True,
            fetch="cursor",
        )
        info = [x._asdict() for x in cursor.fetchall()]
        return {"response": info}
    except Exception as e:
        return None


@app.get("/validators")
def update_validator_classes():
    db = connect_db()
    table_info = db.table_info
    print(table_info)
    validator_classes = sql_to_pydantic(table_info)
    with open("classes.py", "w") as f:
        f.write(validator_classes)
    return "done"
