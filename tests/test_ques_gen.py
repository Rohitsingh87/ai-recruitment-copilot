
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.model import CandidateProfile, JobDescription
from src.interview.question_generator import generate_interview_questions


candidate = CandidateProfile(
    full_name="Rohit Kumar",
    technical_skills=["Python", "FastAPI", "Groq API", "Pydantic"],
)

job = JobDescription(
    job_title="AI Engineer Intern",
    required_skills=["Python", "LLM APIs", "FastAPI", "RAG"],
)

questions = generate_interview_questions(candidate, job)

for index, question in enumerate(questions, start=1):
    print(f"\n{index}. {question.question}")
    print(f"Category: {question.category}")
    print(f"Difficulty: {question.difficulty}")
    print(f"Expected topics: {question.expected_topics}")
