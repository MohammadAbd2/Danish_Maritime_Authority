from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import tempfile
import re


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


def extract_structured_data(text: str) -> Dict[str, Any]:
    """
    Extract structured clinical data from text using regex patterns.
    Returns a dictionary with extracted patient info, vitals, and assessment data.
    """
    extracted = {}
    
    # Patient information patterns
    patient_patterns = {
        'name_title': r'(?:Name|Patient|Navn)[\s:]*([^\n]+)',
        'birthdate_cpr': r'(?:Birthdate|CPR|DOB|Fødselsdato)[\s:]*([^\n]+)',
        'gender': r'(?:Gender|Sex|Køn)[\s:]*([^\n]+)',
        'nationality': r'(?:Nationality|Nationalitet)[\s:]*([^\n]+)',
        'ship_name': r'(?:Ship|Vessel|Skib)[\s:]*([^\n]+)',
        'coordinates': r'(?:Coordinates|Position|Koordinater)[\s:]*([^\n]+)',
    }
    
    # Vitals patterns
    vitals_patterns = {
        'breathing_rate': r'(?:Breathing|Respirat|Resp\.?)[\s:]*(\d+)',
        'oxygen_saturation': r'(?:SpO2|Oxygen sat|O2 sat|Iltmætning)[\s:]*(\d+)',
        'pulse': r'(?:Pulse|Heart rate|HR|Puls)[\s:]*(\d+)',
        'systolic_bp': r'(?:Blood pressure|BP|Blodtryk)[\s:]*(\d+)[\s/\-](\d+)',
        'temperature_mouth': r'(?:Temperature|Temp|Temperatur)[\s:]*(\d+\.?\d*)',
        'blood_sugar': r'(?:Blood sugar|Glucose|Blodsukker)[\s:]*(\d+\.?\d*)',
    }
    
    text_lower = text.lower()
    
    # Extract patient information
    for key, pattern in patient_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted[key] = match.group(1).strip()
    
    # Extract vitals
    for key, pattern in vitals_patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            if key == 'systolic_bp' and match.lastindex >= 2:
                extracted['systolic_bp'] = match.group(1)
                extracted['diastolic_bp'] = match.group(2)
            else:
                try:
                    if key in ('breathing_rate', 'pulse', 'oxygen_saturation'):
                        extracted[key] = int(match.group(1))
                    else:
                        extracted[key] = float(match.group(1))
                except (ValueError, IndexError):
                    pass
    
    # Extract clinical findings and assessment
    if 'airway' in text_lower or 'air way' in text_lower:
        extracted['airway_clear'] = 'clear' in text_lower or 'patent' in text_lower
    
    if 'breathing' in text_lower:
        extracted['breathing_description_fast'] = 'fast' in text_lower or 'tachypnea' in text_lower
        extracted['breathing_description_slow'] = 'slow' in text_lower or 'bradypnea' in text_lower
        extracted['breathing_description_shallow'] = 'shallow' in text_lower
        extracted['breathing_description_deep'] = 'deep' in text_lower
    
    if 'consciousness' in text_lower or 'alert' in text_lower:
        if 'alert' in text_lower and 'oriented' in text_lower:
            extracted['consciousness_level'] = 1
        elif 'responds' in text_lower and 'question' in text_lower:
            extracted['consciousness_level'] = 2
        elif 'responds' in text_lower and 'pain' in text_lower:
            extracted['consciousness_level'] = 3
        elif 'unconscious' in text_lower or 'unresponsive' in text_lower:
            extracted['consciousness_level'] = 4
    
    if 'pupil' in text_lower:
        extracted['pupil_reaction_normal'] = 'normal' in text_lower and 'reactive' in text_lower
    
    # Problem description (usually in first paragraph or after "Problem" keyword)
    prob_match = re.search(r'(?:Problem|Chief complaint|Chief history|Grund)[\s:]*([^\n\n]+)', text, re.IGNORECASE)
    if prob_match:
        extracted['problem_description'] = prob_match.group(1).strip()
    else:
        # Use first few sentences as problem description if not found
        sentences = re.split(r'[.!?]\s+', text)
        if sentences:
            extracted['problem_description'] = sentences[0][:300]
    
    return extracted
