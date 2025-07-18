# agent.py

import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Load your custom prompt from file
with open("prompts/triage_prompt.txt", "r") as f:
    TRIAGE_PROMPT = f.read()

# Create the triage agent
def create_triage_agent():
    llm = ChatOpenAI(
        temperature=0.2,
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    prompt = PromptTemplate(
        input_variables=["report_text"],
        template=TRIAGE_PROMPT
    )

    chain: RunnableSequence = prompt | llm
    return chain
