# Day 8 was uploading the day 7 code to GitHub 
# Day 9
import os
from fastapi import FastAPI
from openai import OpenAI
import time
from pydantic import BaseModel
from dotenv import load_dotenv
import sqlite3

load_dotenv()

def setup_database():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS skills(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       primary_skill TEXT NOT NULL,
                       Proficiency_level TEXT NOT NULL
                   )
                   """)
    conn.commit()
    conn.close()
    
setup_database()

app = FastAPI()

api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    print('API key load successful.')
else:
    print('API load failed.')
    
client = OpenAI()

class ExtractedSkills(BaseModel):
    primary_skill: str
    proficiency_level : str

class TechnicalReport(BaseModel):
    skills:list[ExtractedSkills]

def audit_text_processing(resume_text : str):
    try:
        start_time = time.time()
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                        {"role": "system",'content':'You are a precise backend data parser. Respond concisely.'},
                        {"role": "user", "content": resume_text}
                    ],
            response_format= TechnicalReport
        )
        ai_response = response.choices[0].message.parsed
        end_time = time.time()
        return {
            "data" : ai_response,
            "latency" : end_time - start_time,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens
        }
    except Exception as err:
        print(f'Encontered an error, {err}')
        return None
     
class AuditRequest(BaseModel):
    text : str

@app.post('/audit')
async def run_audit(payload: AuditRequest):
    result = audit_text_processing(payload.text)
    if result:
        for data in result['data'].skills:
            save_skills_to_database(data.primary_skill, data.proficiency_level)
    return result

def save_skills_to_database(primary_skill: str, proficiency_level: str):
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO skills(primary_skill, proficiency_level) VALUES (?, ?)",(primary_skill, proficiency_level))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)