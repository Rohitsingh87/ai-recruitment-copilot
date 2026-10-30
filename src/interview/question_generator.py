
import json

from src.llm.client import get_llm_response
from src.model import CandidateProfile, JobDescription, InterviewQuestion


def generate_interview_questions(
    candidate: CandidateProfile,
    job: JobDescription,
    number_of_questions: int = 5,
) -> list[InterviewQuestion]:

    prompt = f"""
Generate exactly {number_of_questions} interview questions
for this candidate applying for this job.

Candidate skills:
{candidate.technical_skills}

Job title:
{job.job_title}

Required skills:
{job.required_skills}

Return ONLY a valid JSON array.
Each item must contain:
- question: string
- category: string
- difficulty: easy, medium, or hard
- expected_topics: list of strings

Include technical questions relevant to the job.
Do not invent candidate experience.

Return JSON only, without Markdown.
"""

    response = get_llm_response(prompt)

    try:
        data = json.loads(response)

        if not isinstance(data, list):
            raise ValueError("Expected a JSON array of questions.")

        if len(data) != number_of_questions:
            raise ValueError(
                f"Expected {number_of_questions} questions, "
                f"but received {len(data)}."
            )

        return [
            InterviewQuestion.model_validate(item)
            for item in data
        ]

    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"Could not generate valid interview questions: {error}"
        ) from error
