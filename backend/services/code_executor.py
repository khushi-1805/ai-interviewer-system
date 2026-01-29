import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://judge0-ce.p.rapidapi.com/submissions"
HEADERS = {
    "X-RapidAPI-Key": os.getenv("XRAPIDI_KEY"),
    "X-RapidAPI-Host": os.getenv("XRAPIDI_HOST"),
    "Content-Type": "application/json"
}

LANGUAGE_MAP = {
    "python": 71,     # Python 3
    "cpp": 54,        # C++
    "c": 50,
    "java": 62
}

def run_code(source_code: str, language: str, stdin: str = ""):
    payload = {
        "language_id": LANGUAGE_MAP.get(language),
        "source_code": source_code,
        "stdin": stdin
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        params={"base64_encoded": "false", "wait": "true"},
        json=payload
    )

    return response.json()
