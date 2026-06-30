# Day 11 : Comparing cosine similarity between vectors
import os
from openai import OpenAI
from dotenv import load_dotenv
import math

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("API key load failed.")
else:
    print("API key load successful")
    
client = OpenAI()

def calculate_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def generate_vector(text_input: str):
    try:
        response = client.embeddings.create(
            input=text_input,
            model="text-embedding-3-small"
        )
        vector_array = response.data[0].embedding
        return vector_array
    except Exception as err:
        print(f"Encountered: {err}")
    
phrase_1 = "Frontend Web Developer specialising in React"
phrase_2 = "Senior UI/UX Engineer who builds interface"
phrase_3 = "Experienced Cardiothoracic Surgon"

vec_1 = generate_vector(phrase_1)
vec_2 = generate_vector(phrase_2)
vec_3 = generate_vector(phrase_3)

if vec_1 and vec_2 and vec_3:
    score_1_vs_2 = calculate_cosine_similarity(vec_1, vec_2)
    score_2_vs_3 = calculate_cosine_similarity(vec_2, vec_3)
    score_1_vs_3 = calculate_cosine_similarity(vec_1, vec_3)
    
    print("==Results==")
    print(f"Frontend vs UI/UX: {score_1_vs_2:.4f}")
    print(f"UI/UX vs Cardiothoracic: {score_2_vs_3:.4f}")
    print(f"Frontend vs Cardiothoracic: {score_1_vs_3:.4f}")