
import json

from src.llm.client import get_llm_response
from src.model import CandidateProfile


def extract_candidate_profile(resume_text: str) -> CandidateProfile:
    """Extract structured candidate information from resume text."""

    prompt = f"""
Extract candidate information from the resume below.

Return ONLY valid JSON with these keys:
- full_name
- email
- phone
- education
- technical_skills
- projects
- experience
- certifications

Rules:
1. Do not invent or assume information.
2. Use null for missing email or phone.
3. Use empty lists when information is missing.
4. The full_name must be the candidate's actual name from the resume.
5. Return valid JSON only, without Markdown or explanations.
6. For projects, technologies must always be a JSON list of strings,
   for example: ["Python", "Groq API", "Pydantic"].

Resume:
{resume_text}
"""

    response = get_llm_response(prompt)

    try:
        candidate_data = json.loads(response)
        candidate = CandidateProfile.model_validate(candidate_data)
        return candidate

    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"Could not extract valid candidate data: {error}"
        ) from error
