"""
PDF document parser.
Uses PyMuPDF (fitz) with pdfplumber, pypdf, and pytesseract OCR fallbacks.
"""

import structlog
from typing import Optional

logger = structlog.get_logger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract raw text from a PDF file.

    1. Attempts extraction using PyMuPDF (fitz).
    2. Fallback to pdfplumber if fitz fails or is missing.
    3. Fallback to pypdf if pdfplumber fails or is missing.
    4. OCR fallback using pytesseract + Pillow for scanned PDFs.
    """
    text = ""

    # Attempt 1: PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text += page_text + "\n"
        doc.close()

        if text.strip():
            logger.info("PDF text extracted via PyMuPDF", char_count=len(text))
            return text.strip()
    except Exception as e:
        logger.warning("PyMuPDF extraction failed, trying pdfplumber fallback", error=str(e))

    # Fallback 1: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if text.strip():
            logger.info("PDF text extracted via pdfplumber fallback", char_count=len(text))
            return text.strip()
    except Exception as e:
        logger.warning("pdfplumber extraction failed, trying pypdf fallback", error=str(e))

    # Fallback 2: pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        if text.strip():
            logger.info("PDF text extracted via pypdf fallback", char_count=len(text))
            return text.strip()
    except Exception as e:
        logger.warning("pypdf extraction failed", error=str(e))

    # Fallback 3: OCR with pytesseract for image-only/scanned PDFs
    try:
        import fitz
        import pytesseract
        from PIL import Image
        doc = fitz.open(file_path)
        ocr_text = ""
        for page_index in range(len(doc)):
            page = doc[page_index]
            pix = page.get_pixmap(dpi=150)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            page_ocr = pytesseract.image_to_string(img)
            if page_ocr:
                ocr_text += page_ocr + "\n"
        doc.close()

        if ocr_text.strip():
            logger.info("PDF text extracted via pytesseract OCR", char_count=len(ocr_text))
            return ocr_text.strip()
    except Exception as e:
        logger.error("OCR extraction fallback failed", error=str(e))

    return text.strip()
