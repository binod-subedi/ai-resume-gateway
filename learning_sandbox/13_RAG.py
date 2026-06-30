# Day 13/60 -> RAG (Retrieval-Augmented Generation)

import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("API key loaded successfully")
else:
    print("API KEY load failed.")
    
openai_ef = OpenAIEmbeddingFunction(
    api_key= api_key,
    model_name="text-embedding-3-small"    
)
ai_client = OpenAI()

client = chromadb.PersistentClient(path='./candidate_vector')

collection = client.get_or_create_collection(name="resumes", embedding_function=openai_ef)

def recruiter_agent(user_query: str):
    try:
        # RETRIVE 
        results = collection.query(
            query_texts=[user_query],
            n_results=1
        )
        retrieved_text = results["documents"][0][0]
        
        # AUGMENT 
        system_instruction = f"""
        You are an expert technical recruiter assistant. 
        Answer the user's question using ONLY the following context from our candidate database.
        If the answer is not in the context, say "I cannot find a candidate for that."

        CONTEXT:
        {retrieved_text}
        """
        # GENERATE
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system",'content':system_instruction}, {"role": "user", "content": user_query}],
        )
        text_response = response.choices[0].message.content
        return text_response
    
    except Exception as err:
        print(f"Encountered an error: {err}")

query = "We need someone to build a user interface. Who do we have in the database, and what is their specialty?"
answer = recruiter_agent(query)
print("\n=== AGENT RESPONSE ===")
print(answer)