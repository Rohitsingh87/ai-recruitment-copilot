
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pipeline import analyze_candidate


BASE_DIR = Path(__file__).resolve().parents[1]

resume_path = (
    BASE_DIR
    / "data"
    / "sample_resumes"
    / "Rohit_Kumar_AI_Engineer_Resume.pdf"
)

job_description = """
Job Title: AI Engineer Intern
Company: Example AI Technologies

Required Skills:
- Python
- LLM APIs
- RAG
- FastAPI
- Pydantic

Responsibilities:
- Build AI-powered applications
- Develop and test LLM features
- Create and evaluate RAG pipelines

Experience: 0-1 years
Education: Bachelor's degree in Computer Science or a related field.
"""

report = analyze_candidate(
    resume_path=str(resume_path),
    job_text=job_description,
)

print("\n========== RECRUITMENT REPORT ==========\n")
print(report.model_dump_json(indent=2))
print("\n========== ANALYSIS COMPLETE ==========")
