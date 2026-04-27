from pathlib import Path
from typing import Tuple
import tempfile


def extract_text(filename: str, content: bytes) -> Tuple[str, str]:
    suffix = Path(filename).suffix.lower()
    if suffix == ".txt":
        return content.decode("utf-8", errors="ignore"), "txt"
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                f.write(content)
                path = f.name
            reader = PdfReader(path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text, "pdf"
        except Exception as e:
            return f"PDF text extraction failed: {e}", "pdf-error"
    if suffix == ".docx":
        try:
            from docx import Document
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
                f.write(content)
                path = f.name
            doc = Document(path)
            text = "\n".join(p.text for p in doc.paragraphs)
            return text, "docx"
        except Exception as e:
            return f"DOCX text extraction failed: {e}", "docx-error"
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}:
        try:
            from PIL import Image
            import pytesseract
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
                f.write(content)
                path = f.name
            text = pytesseract.image_to_string(Image.open(path))
            return text, "ocr-image"
        except Exception as e:
            return "OCR is configured in the code, but Tesseract/Pillow could not process this image. Install tesseract-ocr and pytesseract. Error: " + str(e), "ocr-error"
    return "Unsupported file type. Supported: PDF, DOCX, TXT, PNG/JPG scanned reports.", "unsupported"
