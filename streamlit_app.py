from src.mcqgenerator.utils import get_table_data, read_file
from src.mcqgenerator.logger import get_logger
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import json
from langchain.callbacks import get_openai_callback
import traceback

load_dotenv()

logger = get_logger()

with open(Path("response.json")) as json_file:
    response_json: dict = json.load(json_file)

st.title("MCQs Creator Application with LangChain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload PDF or a TXT file")
    
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    
    subject = st.text_input("Insert Subject", max_chars=20)
    
    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")
    
    button = st.form_submit_button("Create MCQs")
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                
                # How to setup token usage Tracking in Langchain
                with get_openai_callback() as cb: 
                    response = generate_evaluate_chain.invoke({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(response_json)  
                    })
                
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print("Total cost:", cb.total_cost)
                print("Total tokens:", cb.total_tokens)
                print("Prompt tokens:", cb.prompt_tokens)
                print("Completion tokens:", cb.completion_tokens)
                print("Successful requests:", cb.successful_requests)
            
                if isinstance(response, dict):
                    quiz = response.get("quiz")
                
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                    
                else:
                    st.write(response)
