import traceback
from pypdf import PdfReader
from pathlib import Path
import pandas as pd
import json

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error handling the PDF file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception(
            "Unsupported file format only pdf and text files supported"
        )

def get_table_data(quiz_str):
    json_quiz = json.loads(quiz_str)

    quiz_table_data = []

    for _, value in json_quiz.items():
        quiz_table_data.append({
            "MCQ": value["mcq"],
            "options": " | ".join([f"{option} : {option_value}" for option, option_value in value["options"].items()]),
            "correct": value["correct"]
        })

    return quiz_table_data
