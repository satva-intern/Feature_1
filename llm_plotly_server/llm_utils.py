import os
import requests
from dotenv import load_dotenv
load_dotenv()


GROQ_API_KEY = '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'
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_llm(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen/qwen3-32b",  # or "llama3-8b-8192"
        "messages": [
            {"role": "system", "content": "You are a data analyst who writes Python code using Plotly."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()['choices'][0]['message']['content']
