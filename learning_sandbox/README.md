# AI Resume Processing Gateway

A high-performance REST API built with FastAPI that ingests unstructured candidate profiles and uses LLM constrained decoding (Pydantic + OpenAI) to extract structured technical skills.

## Architecture

- **Framework:** FastAPI
- **AI Engine:** OpenAI (gpt-4o-mini)
- **Data Validation:** Pydantic (Strict JSON enforcement)
- **Telemetry:** Built-in latency and token tracking.

## Local Setup

1. Clone the repository.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install requirements: `pip install fastapi uvicorn openai python-dotenv pydantic`
5. Create a `.env` file and add your OpenAI Key: `OPENAI_API_KEY=your_key`
6. Run the server: `python3 07_REST_API_gateway.py`

## Endpoint Documentation

### POST `/audit`

Extracts technical skills and calculates execution latency.

**Request Payload:**

```json
{
  "text": "Expert frontend engineer proficient in ReactJS."
}
```

**Response Payload:**

```json
{
  "data": {
    "skills": [
      {
        "skill_name": "ReactJS",
        "proficiency_level": "Expert"
      }
    ]
  },
  "latency_seconds": 1.25,
  "input_tokens": 120,
  "output_tokens": 15
}
```
