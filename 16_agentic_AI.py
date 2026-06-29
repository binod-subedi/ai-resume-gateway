# Day 16 : Agentic AI - Routing 
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

load_dotenv()

client = OpenAI()

class RouteDecision(BaseModel):
    destination: Literal["DATABASE_SEARCH", "GENERAL_CHAT"]
    
def triangle_prompt(user_input: str):
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
                {"role": "system",'content':"You are an intent classification router. If the user asks about hiring, candidates, or resumes, route to 'DATABASE_SEARCH'. If it is casual conversation or general knowledge, route to 'GENERAL_CHAT'."},
                {"role": "user", "content": user_input}
            ],
        response_format=RouteDecision
    )
    ai_said = response.choices[0].message.parsed.destination
    return ai_said

# Dummy Functions to Check if Router mechanic is working or not.
def handle_database(query: str):
    print(f"[EXECUTING] Searching Vector DB for: '{query}'...")

def handle_chat(query: str):
    print(f"[EXECUTING] Streaming casual chat for: '{query}'...")
    
if __name__ == "__main__":
    print("=== MULTI-AGENT ROUTER INITIALIZED ===")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit','exit']:
            break
        decision = triangle_prompt(user_input)
        print(f'Router Decision {decision}')
        
        if decision == "DATABASE_SEARCH":
            handle_database(user_input) 
        elif decision =="GENERAL_CHAT":
            handle_chat(user_input)