
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from all pages of a PDF file."""
    reader = PdfReader(pdf_path)

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    return extracted_text.strip()
