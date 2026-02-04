from PyPDF2 import PdfReader
import io

def extract_text_from_pdf_bytes(pdf_bytes):
    """Extract text from PDF bytes"""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text