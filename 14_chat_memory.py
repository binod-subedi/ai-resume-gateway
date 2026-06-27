import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ChatSession:
    def __init__(self, max_window_turns: int = 3):
        self.client = OpenAI()
        self.model = "gpt-4o-mini"
        self.max_window_turns = max_window_turns
        self.history = []
        self.system_message = {"role": "system", "content": "You are a helpful programming assistant."}
    
    def send_message(self, user_text : str) -> str:
        self.history.append({"role":"user", "content": user_text})
        
        max_messages = self.max_window_turns * 2
        if len(self.history) >  max_messages:
            self.history = self.history[-max_messages:]
            
        payload = [self.system_message] + self.history
        
        try:
            response = self.client.chat.completions.create(
                model= self.model,
                messages=payload
            )
            ai_reply = response.choices[0].message.content
            self.history.append({"role": "assistant", "content":ai_reply})
            return ai_reply
        except Exception as err:
            return f'Error: {err}'

if __name__== "__main__":
    session = ChatSession(max_window_turns=2)
    print("=== STATEFUL AI CHAT SESSION INITIALIZED ===")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Session Ending")
            break
        
        if not user_input.strip():
            continue
        
        reply = session.send_message(user_input)
        print(f"\nAI: {reply}\n")    