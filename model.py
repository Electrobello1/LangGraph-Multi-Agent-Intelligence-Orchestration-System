import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_llm_response(prompt: str):

    payload = {
        "model": "gpt-oss:120b-cloud",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:
        return f"LLM Error: {str(e)}"