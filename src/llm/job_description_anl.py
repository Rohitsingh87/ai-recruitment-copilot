
import json

from src.llm.client import get_llm_response
from src.model import JobDescription


def analyze_job_description(job_text: str) -> JobDescription:
    """Extract structured information from a job description."""

    prompt = f"""
Analyze the job description below.

Return ONLY valid JSON with these keys:
- job_title
- company_name
- required_skills (list of strings)
- preferred_skills (list of strings)
- responsibilities (list of strings)
- experience_required
- education_required

Rules:
1. Do not invent information.
2. Use null if the company, experience, or education requirement is missing.
3. Use empty lists if skills or responsibilities are missing.
4. All skills and responsibilities must be lists of strings.
5. Return JSON only, without Markdown.

Job description:
{job_text}
"""

    response = get_llm_response(prompt)

    try:
        job_data = json.loads(response)
        return JobDescription.model_validate(job_data)
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"Could not analyze job description: {error}"
        ) from error
