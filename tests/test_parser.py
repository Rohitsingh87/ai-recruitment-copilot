import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.resume_parser.parser import extract_text_from_pdf

pdf_path = "data/sample_resumes/Rohit_Kumar_AI_Engineer_Resume.pdf"

text = extract_text_from_pdf(pdf_path)
print(text)