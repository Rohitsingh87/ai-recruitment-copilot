
from src.resume_parser.parser import extract_text_from_pdf
from src.llm.resume_extractor import extract_candidate_profile
from src.llm.job_description_anl import analyze_job_description
from src.matching.skill_matcher import match_skills
from src.interview.question_generator import generate_interview_questions
from src.model import RecruitmentAnalysis


def analyze_candidate(resume_path: str, job_text: str) -> RecruitmentAnalysis:
    """Run the complete recruitment analysis pipeline."""

    # 1. Extract resume text
    resume_text = extract_text_from_pdf(resume_path)

    # 2. Extract candidate profile
    candidate = extract_candidate_profile(resume_text)

    # 3. Analyze job description
    job = analyze_job_description(job_text)

    # 4. Match candidate skills against job requirements
    skill_match = match_skills(candidate, job)

    # 5. Generate interview questions
    questions = generate_interview_questions(candidate, job)

    # 6. Build the final report
    return RecruitmentAnalysis(
        candidate=candidate,
        job=job,
        skill_match=skill_match,
        interview_questions=questions,
        summary=(
            f"{candidate.full_name} has a "
            f"{skill_match.match_percentage}% exact skill match "
            f"for the role of {job.job_title}."
        ),
        recommendations=[
            f"Review missing skill: {skill}"
            for skill in skill_match.missing_skills
        ],
    )
