import re

from utils import sql_to_pydantic

test_str = """CREATE TABLE `Case_setup_trig_emg` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `pedicle_screw` tinyint(1) DEFAULT NULL,
  `direct_nerve_stim` tinyint(1) DEFAULT NULL,
  `guidance` tinyint(1) DEFAULT NULL,
  `other` tinyint(1) DEFAULT NULL,
  `place_ground` text,
  `proble_type` text,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `trig_emg_setup_fk` FOREIGN KEY (`patient_id`) REFERENCES `PatientInfo` (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE `PatientInfo` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Gender` enum('Male','Female','Other') NOT NULL,
  `DateOfBirth` date NOT NULL,
  `Height` int NOT NULL,
  `Weight` int NOT NULL,
  `InsuranceType` enum('Private','Medicare','Medicaid','VA') DEFAULT 'Private' NOT NULL ,
  `PolicyNumber` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `MedicalRecord` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `HospitalRecord` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`patient_id`),
  CONSTRAINT `chk_gender` CHECK ((`Gender` in (_utf8mb4'Male',_utf8mb4'Female',_utf8mb4'Other')))
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"""


import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Body(BaseModel):
    sql: str


@app.post("/api")
async def get(sql: Body):
    return sql_to_pydantic(sql.sql)


@app.get("/")
async def root() -> HTMLResponse:
    return HTMLResponse(
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converter</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.6/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.6/theme/monokai.min.css">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #272822;
            color: #f8f8f2;
        }
        .container {
            width: 100%;
            max-width: 80vw;
        }
        .textbox-container {
            display: flex;
        }
        .CodeMirror {
            width: 50%;
            height: 92vh;
            background-color: #272822;
            color: #f8f8f2;
            border: 1px solid #75715e;
            position: relative;
        }
        .CodeMirror-placeholder {
            color: #75715e;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #75715e;
            border: none;
            color: #f8f8f2;
        }
        button:hover {
            background-color: #a6e22e;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="textbox-container">
            <textarea id="leftBox" placeholder="Enter SQL here..."></textarea>
            <textarea id="rightBox" placeholder="Output will appear here..."></textarea>
        </div>
        <div class="button-container">
            <button onclick="convertText()">Convert</button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.6/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.6/mode/sql/sql.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.6/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.6/addon/display/placeholder.min.js"></script>
    <script>
        // Initialize CodeMirror editors
        const leftBox = CodeMirror.fromTextArea(document.getElementById('leftBox'), {
            mode: 'text/x-sql',
            theme: 'monokai',
            lineNumbers: true,
            placeholder: 'Enter SQL here...'
        });

        const rightBox = CodeMirror.fromTextArea(document.getElementById('rightBox'), {
            mode: 'text/x-python',
            theme: 'monokai',
            lineNumbers: true,
            readOnly: true,
            placeholder: 'Output will appear here...'
        });

        async function convertText() {
            const input = leftBox.getValue();
            console.log('Input:', input);  // Debug log

            try {
                const response = await fetch('/api', {  // Ensure this URL is correct
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ sql: input })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                console.log('Response Data:', data);  // Debug log
                rightBox.setValue(data);
            } catch (error) {
                console.error('Error:', error);  // Debug log
                rightBox.setValue('Error: ' + error.message);
            }
        }
    </script>
</body>
</html>

"""
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
