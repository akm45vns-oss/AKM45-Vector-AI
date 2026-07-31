"""
Text cleaning and normalization module.
Removes control characters, normalizes whitespace, detects language, and prepares text for NLP.
"""

import re
import unicodedata
from typing import Optional
import structlog
from langdetect import detect, LangDetectException

logger = structlog.get_logger(__name__)


def clean_text(raw_text: str) -> str:
    """
    Clean and normalize raw extracted document text.
    - Normalizes unicode characters
    - Removes non-printable control characters
    - Normalizes multi-spaces and empty lines
    """
    if not raw_text:
        return ""

    # Unicode normalization (NFKC)
    text = unicodedata.normalize("NFKC", raw_text)

    # Replace strange quotes/dashes with standard ASCII
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    text = text.replace("–", "-").replace("—", "-")

    # Remove non-printable control characters (except newline, tab)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)

    # Normalize horizontal whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize vertical whitespace (max 2 consecutive newlines)
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def detect_document_language(text: str) -> str:
    """
    Detect the primary language of the text.
    Returns ISO 639-1 code (e.g., 'en', 'es'). Defaults to 'en'.
    """
    if not text or len(text.strip()) < 20:
        return "en"

    try:
        lang = detect(text[:2000])
        return lang
    except LangDetectException:
        logger.warning("Language detection failed, defaulting to 'en'")
        return "en"
