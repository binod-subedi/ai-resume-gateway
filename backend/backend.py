# IMPORTS
import os
import uvicorn
import chromadb
from openai import AsyncOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from fastapi.responses import StreamingResponse


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

openai_ef = OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-3-small"
)
db_client = chromadb.PersistentClient(path='./candidate_vector')
collection = db_client.get_or_create_collection('resumes', embedding_function=openai_ef)


app = FastAPI()
aclient = AsyncOpenAI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message : str

async def generate_rag_system(user_query: str):
    #RETRIVE
    results = collection.query(query_texts=[user_query], n_results=1)
    retrieved_text = ""
    if results["documents"] and len(results["documents"]) > 0:
        retrieved_text = results["documents"][0][0]
    
    print(f"\n--- DEBUG: DATABASE FOUND ---\n{retrieved_text}\n-----------------------------\n")
    #AUGMENT
    system_instruction = f"""
    You are an expert technical recruiter assistant. 
    Answer the user's question using ONLY the following context from our candidate database.
    If the answer is not in the context, say "I cannot find a candidate for that."
    
    CONTEXT:
    {retrieved_text}
    """
    
    #GENERATE
    response = await aclient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content":system_instruction},
            {"role":"user", "content":user_query}
        ],
        stream=True
    )
    
    async for chunk in response:
        text = chunk.choices[0].delta.content
        if text:
            yield text
            
@app.post("/chat")
async def handle_chat(payload:ChatRequest):
    return StreamingResponse(generate_rag_system(payload.message), media_type="text/event-stream")
    
if __name__ == "__main__":
    uvicorn.run(app,  host="127.0.0.1", port=8000)