# Day 12: Experiment of Vector DB 
import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

openai_ef = OpenAIEmbeddingFunction(
    api_key= api_key,
    model_name="text-embedding-3-small"    
)

client = chromadb.PersistentClient(path="./candidate_vector")
collection = client.get_or_create_collection(name="resumes", embedding_function=openai_ef)

collection.upsert(
    documents=[
        "Frontend Web Developer specializing in React",
        "Senior Backend Engineer with Python and PostgreSQL",
        "Cardiothoracic Surgeon with 10 years experience"
    ],
    ids=["candidate_1", "candidate_2", "candidate_3"]
)

results = collection.query(
    query_texts=["Need someone to design and build user interfaces"],
    n_results=1
)

print(results)