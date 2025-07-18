# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_triage_agent
import uvicorn

# Create the FastAPI app
app = FastAPI()

# Create the AI agent
triage_agent = create_triage_agent()

# Define the input format
class BugReport(BaseModel):
    report_text: str

# Define the endpoint
@app.post("/triage")
def triage_report(bug: BugReport):
    result = triage_agent.invoke({"report_text": bug.report_text})
    

    # Extract just the clean response text
    if hasattr(result, "content"):
        return {"triage_result": result.content.replace("\n", "<br>")}
    return {"triage_result": str(result)}
