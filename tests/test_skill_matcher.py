
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.model import CandidateProfile, JobDescription
from src.matching.skill_matcher import match_skills


candidate = CandidateProfile(
    full_name="Rohit Kumar",
    technical_skills=[
        "Python",
        "FastAPI",
        "Groq API",
        "Pydantic"
    ]
)

job = JobDescription(
    job_title="AI Engineer Intern",
    required_skills=[
        "Python",
        "LLM APIs",
        "FastAPI",
        "RAG"
    ]
)

result = match_skills(candidate, job)

print("\nSkill Match Result:")
print(result.model_dump_json(indent=2))
