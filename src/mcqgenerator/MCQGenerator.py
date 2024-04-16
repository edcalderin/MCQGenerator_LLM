import os
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
 
load_dotenv()

KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model='gpt-3.5-turbo', temperature = 0.3, api_key = KEY)

TEMPLATE = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to create a a quiz of {number} 
multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs.

### RESPONSE_JSON
{response_json} 
"""

quiz_generation_prompt = PromptTemplate(
    input_variables = ["text", "number", "subject", "tone", "response_json"],
    template = TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2: str = """
You are an expert english grammarian and writer. Given a a Multiple Choice Quiz for {subject} students.
You need to evaluate the complexity of the questions and give a complete analysis of the quiz. Only use up max 50 words for complexity
if the quiz is not at per with the cognitive and analytical abilities of the students,
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the students abilities.
MCQ Quiz:
{quiz}

Check from an expert English writer of the above quiz.
"""

review_prompt = PromptTemplate(
    input_variables = ["subject", "quiz"],
    template = TEMPLATE2
)

review_chain = LLMChain(llm=llm, prompt=review_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(
    chains = [quiz_chain, review_chain], 
    input_variables = ["text", "number", "subject", "tone", "response_json"],
    output_variables = ["quiz", "review"],
    verbose=True
)
