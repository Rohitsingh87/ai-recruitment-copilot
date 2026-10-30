
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.llm.resume_extractor import extract_candidate_profile
from src.resume_parser.parser import extract_text_from_pdf


resume_path = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "sample_resumes"
    / "Rohit_Kumar_AI_Engineer_Resume.pdf"
)

resume_text = extract_text_from_pdf(str(resume_path))
candidate = extract_candidate_profile(resume_text)

print("\nExtracted Candidate Profile:")
print(candidate.model_dump_json(indent=2))
