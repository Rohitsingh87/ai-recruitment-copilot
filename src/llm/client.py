
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )

client = Groq(api_key=api_key)


def get_llm_response(prompt: str) -> str:
    """Send a prompt to Groq and return the model's response."""
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI recruitment assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content or ""
