"""
Full resume entity extractor module.
Extracts contact details, experience years, education, links, structured skills, and enterprise AI insights.
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
    Extract candidate name using spaCy PERSON entity recognition with fallback regex.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()][:6]
    
    for line in lines:
        clean_line = re.sub(r"[^\w\s]", "", line).strip()
        if not clean_line or any(w.lower() in ["dream", "cv", "resume", "curriculum", "vitae", "phone", "email", "location"] for w in clean_line.split()):
            continue
        words = clean_line.split()
        if 2 <= len(words) <= 4 and not re.search(r"[\d@]", line):
            return clean_line.title()

    nlp = get_nlp_model()
    doc = nlp(" ".join(lines))
    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
            return ent.text.strip().title()

    return None


def generate_enterprise_insights(text: str, name: Optional[str], skills: List[str], years_exp: float) -> Dict[str, Any]:
    """
    Generate enterprise-grade AI insights, key strengths, gap analysis, and screening questions.
    """
    cand_name = name or "Candidate"
    
    # 1. Experience Level Classification
    if years_exp >= 7.0:
        exp_level = "Principal / Lead Engineer"
    elif years_exp >= 4.0:
        exp_level = "Senior Specialist"
    elif years_exp >= 1.5:
        exp_level = "Mid-Level Professional"
    else:
        exp_level = "Associate / Early Career Specialist"

    # 2. Recommended Roles
    roles = []
    text_lower = text.lower()
    if any(k in text_lower for k in ["machine learning", "ai", "model", "trainer", "python", "nlp"]):
        roles.append("AI/ML Engineer & Model Trainer")
    if any(k in text_lower for k in ["fastapi", "django", "flask", "backend", "api", "sql"]):
        roles.append("Backend Systems Engineer")
    if any(k in text_lower for k in ["react", "next.js", "javascript", "typescript", "frontend"]):
        roles.append("Full-Stack Software Developer")
    if not roles:
        roles = ["Software Engineer", "Technical Specialist"]

    # 3. Key Strengths
    strengths = []
    if "python" in text_lower or "machine learning" in text_lower:
        strengths.append("Strong Python & Artificial Intelligence foundation with hands-on model training experience")
    if any(k in text_lower for k in ["github", "git"]):
        strengths.append("Active open-source version control & collaborative codebase contributions")
    if any(k in text_lower for k in ["sql", "database"]):
        strengths.append("Proficiency in relational databases and structured query optimization")
    if len(strengths) < 3:
        strengths.append("Clean document structure with clear technical competencies and project highlights")

    # 4. Recommended Missing Skills
    missing_skills = []
    if "docker" not in text_lower and "kubernetes" not in text_lower:
        missing_skills.append("Containerization (Docker & Kubernetes)")
    if "aws" not in text_lower and "cloud" not in text_lower and "azure" not in text_lower:
        missing_skills.append("Cloud Infrastructure (AWS / GCP / Azure)")
    if "pytest" not in text_lower and "testing" not in text_lower:
        missing_skills.append("Automated Testing Frameworks (Pytest / Jest)")

    # 5. Interview Screening Questions
    questions = [
        f"Can you walk us through a recent machine learning or software project you built using Python?",
        f"How do you approach optimizing database queries and handling API state management in production applications?",
        f"What strategies do you use for model evaluation, error tracking, and maintaining clean code architecture?",
    ]

    # 6. Executive Summary
    skills_str = ", ".join(skills[:6]) if skills else "core technical competencies"
    summary = (
        f"{cand_name} is a {exp_level} with demonstrated expertise in {skills_str}. "
        f"The candidate displays strong analytical proficiency, clean codebase organization, "
        f"and high alignment for {', '.join(roles[:2])} positions."
    )

    return {
        "experience_level": exp_level,
        "recommended_roles": roles,
        "key_strengths": strengths,
        "missing_skills": missing_skills,
        "interview_questions": questions,
        "executive_summary": summary,
    }


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

    # Generate enterprise intelligence
    insights = generate_enterprise_insights(cleaned, name, all_extracted_skills, years_exp)

    parsed_data = {
        "candidate_name": name,
        "email": email,
        "phone": phone,
        "linkedin": socials["linkedin"],
        "github": socials["github"],
        "years_of_experience": years_exp,
        "skills_by_category": skills,
        "extracted_skills": all_extracted_skills,
        "enterprise_insights": insights,
    }

    logger.info("Enterprise resume parsing complete", candidate_name=name, email=email, total_skills=len(all_extracted_skills))
    return parsed_data
