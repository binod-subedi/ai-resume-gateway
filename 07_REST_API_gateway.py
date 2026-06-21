import os
from fastapi import FastAPI
from openai import OpenAI
import time
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

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
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)