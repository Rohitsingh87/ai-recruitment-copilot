
import re

from src.model import CandidateProfile, JobDescription, SkillMatch


def normalize_skill(skill: str) -> str:
    """Convert related skill names into a common label."""
    skill = skill.lower().strip()

    # Remove common proficiency labels.
    skill = re.sub(r"\s*\((basic|beginner|intermediate|advanced)\)\s*", "", skill)
    skill = re.sub(r"[^a-z0-9+#. ]", " ", skill)
    skill = re.sub(r"\s+", " ", skill).strip()

    # FastAPI variations.
    if "fastapi" in skill:
        return "fastapi"

    # LLM API variations.
    if (
        "llm api" in skill
        or "llm apis" in skill
        or "groq api" in skill
    ):
        return "llm apis"

    # RAG variations.
    if re.search(r"\brag\b", skill):
        return "rag"

    return skill


def match_skills(
    candidate: CandidateProfile,
    job: JobDescription
) -> SkillMatch:
    """Match candidate skills against job requirements."""

    candidate_skills = candidate.technical_skills
    required_skills = job.required_skills

    # Normalize skills for comparison.
    candidate_normalized = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    matched = []
    missing = []

    for required_skill in required_skills:
        normalized_required = normalize_skill(required_skill)

        if normalized_required in candidate_normalized:
            matched.append(required_skill)
        else:
            missing.append(required_skill)

    # Keep original candidate skill names in additional skills.
    matched_normalized = {
        normalize_skill(skill) for skill in matched
    }

    additional = [
        skill
        for skill in candidate_skills
        if normalize_skill(skill) not in {
            normalize_skill(req) for req in required_skills
        }
    ]

    # Calculate percentage based on required skills satisfied.
    if not required_skills:
        percentage = 0.0
    else:
        percentage = round(
            len(matched) / len(required_skills) * 100,
            2
        )

    return SkillMatch(
        matched_skills=matched,
        missing_skills=missing,
        additional_skills=additional,
        match_percentage=percentage
    )
