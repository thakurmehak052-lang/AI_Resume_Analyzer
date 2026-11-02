
from pypdf import PdfReader
from io import BytesIO


def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.getvalue()
    reader = PdfReader(BytesIO(pdf_bytes))

    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    return text.strip()
