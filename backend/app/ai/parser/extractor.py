"""
Full resume entity extractor module.
Extracts contact details, experience years, education, links, and structured skills.
"""

import re
from typing import Any, Dict, List, Optional
import structlog

from app.ai.parser.skill_extractor import extract_skills, get_nlp_model
from app.ai.parser.text_cleaner import clean_text

logger = structlog.get_logger(__name__)

# Regex Patterns
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
LINKEDIN_REGEX = r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+"
GITHUB_REGEX = r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+"
YEARS_EXP_REGEX = r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)?"


def extract_email(text: str) -> Optional[str]:
    match = re.search(EMAIL_REGEX, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    match = re.search(PHONE_REGEX, text)
    return match.group(0) if match else None


def extract_social_links(text: str) -> Dict[str, Optional[str]]:
    linkedin = re.search(LINKEDIN_REGEX, text, re.IGNORECASE)
    github = re.search(GITHUB_REGEX, text, re.IGNORECASE)
    return {
        "linkedin": linkedin.group(0) if linkedin else None,
        "github": github.group(0) if github else None,
    }


def extract_years_of_experience(text: str) -> float:
    """Extract total years of experience mentioned in resume."""
    matches = re.findall(YEARS_EXP_REGEX, text, re.IGNORECASE)
    if matches:
        try:
            years = [float(m) for m in matches]
            return max(years)
        except ValueError:
            pass
    return 0.0


def extract_name(text: str) -> Optional[str]:
    """
    Extract candidate name using spaCy PERSON entity recognition.
    Prioritizes PERSON entity found in the first 5 lines of the resume.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()][:5]
    header_text = " ".join(lines)

    nlp = get_nlp_model()
    doc = nlp(header_text)

    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
            return ent.text.strip()

    # Fallback: Use line 1 if it looks like a clean name
    if lines:
        first_line = lines[0]
        if len(first_line.split()) in [2, 3] and not re.search(r"[@\d]", first_line):
            return first_line.title()

    return None


def parse_resume_content(raw_text: str) -> Dict[str, Any]:
    """
    Master function to parse all structured data from clean resume text.
    """
    cleaned = clean_text(raw_text)

    name = extract_name(cleaned)
    email = extract_email(cleaned)
    phone = extract_phone(cleaned)
    socials = extract_social_links(cleaned)
    years_exp = extract_years_of_experience(cleaned)
    skills = extract_skills(cleaned)

    # Aggregate flat skill list
    all_extracted_skills = sorted(list({s for cat in skills.values() for s in cat}))

    parsed_data = {
        "candidate_name": name,
        "email": email,
        "phone": phone,
        "linkedin": socials["linkedin"],
        "github": socials["github"],
        "years_of_experience": years_exp,
        "skills_by_category": skills,
        "extracted_skills": all_extracted_skills,
    }

    logger.info("Resume parsing complete", candidate_name=name, email=email, total_skills=len(all_extracted_skills))
    return parsed_data
