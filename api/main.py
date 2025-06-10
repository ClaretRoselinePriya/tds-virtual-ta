from fastapi import FastAPI
from pydantic import BaseModel
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
openai.api_key = os.getenv("OPEN_API_KEY")

class Query(BaseModel):
    question: str
    image: str = None

@app.post("/api/")
async def answer_question(query: Query):
    context = load_context()  # Load scraped data
    response = ask_gpt(query.question, context)
    return response

def load_context():
    with open("data/tds_kb_data.json", "r") as f:
        data = json.load(f)
    return json.dumps(data)[:8000]

def ask_gpt(question, context):
    prompt = f"""
You are a TDS virtual TA. Use the following course and discourse content:

{context}

Student question:
{question}

Provide your answer with any relevant links.
"""
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )
    return {"answer": completion['choices'][0]['message']['content'], "links": []}
