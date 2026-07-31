"""
Unit tests for resume parser modules (text cleaner, skill extractor, entity extractor).
"""

import pytest
from app.ai.parser.text_cleaner import clean_text, detect_document_language
from app.ai.parser.skill_extractor import extract_skills
from app.ai.parser.extractor import (
    extract_email,
    extract_phone,
    extract_social_links,
    extract_years_of_experience,
    parse_resume_content,
)


def test_clean_text():
    sample = "  Hello   World!\n\n\n\nThis is a test.   "
    cleaned = clean_text(sample)
    assert "  " not in cleaned
    assert "\n\n\n" not in cleaned
    assert cleaned.startswith("Hello")


def test_detect_language():
    sample_en = "Senior Software Engineer with 5 years of experience building Python and React applications."
    assert detect_document_language(sample_en) == "en"


def test_extract_contact_info():
    sample_text = """
    John Doe
    Email: john.doe@example.com
    Phone: +1 (555) 123-4567
    LinkedIn: linkedin.com/in/johndoe
    GitHub: github.com/johndoe
    """
    assert extract_email(sample_text) == "john.doe@example.com"
    assert extract_phone(sample_text) == "+1 (555) 123-4567"
    socials = extract_social_links(sample_text)
    assert socials["linkedin"] == "linkedin.com/in/johndoe"
    assert socials["github"] == "github.com/johndoe"


def test_extract_years_of_experience():
    text = "Accomplished Engineer with 7+ years of experience in cloud infrastructure."
    assert extract_years_of_experience(text) == 7.0


def test_extract_skills():
    text = "Proficient in Python, FastAPI, PostgreSQL, Docker, Kubernetes, AWS, and React."
    skills = extract_skills(text)
    assert "python" in skills["programming_languages"]
    assert "fastapi" in skills["frameworks"]
    assert "postgresql" in skills["databases"]
    assert "docker" in skills["cloud"]
    assert "kubernetes" in skills["cloud"]
    assert "aws" in skills["cloud"]
    assert "react" in skills["frameworks"]


def test_parse_resume_content():
    raw_resume = """
    Alice Smith
    alice.smith@techcorp.com
    +1-555-987-6543
    linkedin.com/in/alicesmith

    Summary
    Senior Full Stack Developer with 6 years of experience.

    Skills
    Python, TypeScript, Next.js, Django, PostgreSQL, Docker, Git, Agile
    """
    parsed = parse_resume_content(raw_resume)
    assert parsed["candidate_name"] is not None
    assert parsed["email"] == "alice.smith@techcorp.com"
    assert parsed["years_of_experience"] == 6.0
    assert "python" in parsed["extracted_skills"]
    assert "typescript" in parsed["extracted_skills"]
    assert "next.js" in parsed["extracted_skills"]
