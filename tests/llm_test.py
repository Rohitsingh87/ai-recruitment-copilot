
print("Test started")

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

print("Importing LLM client...")

from src.llm.client import get_llm_response

print("Import successful")
print("Calling Groq API...")

answer = get_llm_response(
    "Reply with exactly: Groq connection successful"
)

print("Response received:")
print(repr(answer))
