
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.llm.job_description_anl import analyze_job_description


sample_job = """
Job Title: AI Engineer Intern
Company: Example AI Technologies

Requirements:
- Python programming
- Experience with LLM APIs
- Knowledge of RAG and embeddings
- Familiarity with FastAPI

Responsibilities:
- Build AI-powered applications
- Develop and test LLM features

Experience: 0-1 years
Education: Bachelor's degree in Computer Science or a related field.
"""

job = analyze_job_description(sample_job)

print("\nAnalyzed Job Description:")
print(job.model_dump_json(indent=2))
