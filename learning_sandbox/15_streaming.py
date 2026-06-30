import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API key load successful")
else:
    print("API key load failed.")
    
client = OpenAI()

def call_ai(user_input : str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user", "content":user_input}],
            stream=True
        )
        
        for event in response:
            text = event.choices[0].delta.content
            if text:
                print(text, end="", flush=True)
        
    except Exception as err:
        print(f'Encountered error(s): {err}')

user_input = input("You: ")
call_ai(user_input)