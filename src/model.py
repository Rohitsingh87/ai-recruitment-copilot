
from pydantic import BaseModel, Field, AliasChoices, model_validator, field_validator


class Education(BaseModel):
    degree: str | None = None
    institution: str | None = None
    year: int | None = None
    cgpa: str | None = None

    @model_validator(mode="before")
    @classmethod
    def convert_string(cls, value):
        if isinstance(value, str):
            return {"degree": value}
        return value


class Project(BaseModel):
    name: str
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)

    @field_validator("technologies", mode="before")
    @classmethod
    def convert_technologies(cls, value):
        if isinstance(value, str):
            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]
        return value


class Certification(BaseModel):
    name: str = Field(
        validation_alias=AliasChoices("name", "title")
    )
    provider: str | None = Field(
        default=None,
        validation_alias=AliasChoices("provider", "issuer")
    )
    year: int | None = None

    @model_validator(mode="before")
    @classmethod
    def convert_string(cls, value):
        if isinstance(value, str):
            return {"name": value}
        return value


class CandidateProfile(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    education: list[Education] = Field(default_factory=list)
    technical_skills: list[str] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)


class JobDescription(BaseModel):
    job_title: str
    company_name: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    experience_required: str | None = None
    education_required: str | None = None


class SkillMatch(BaseModel):
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    additional_skills: list[str] = Field(default_factory=list)
    match_percentage: float = 0.0


class InterviewQuestion(BaseModel):
    question: str
    category: str
    difficulty: str = "medium"
    expected_topics: list[str] = Field(default_factory=list)


class RecruitmentAnalysis(BaseModel):
    candidate: CandidateProfile
    job: JobDescription
    skill_match: SkillMatch
    interview_questions: list[InterviewQuestion] = Field(default_factory=list)
    summary: str = ""
    recommendations: list[str] = Field(default_factory=list)
