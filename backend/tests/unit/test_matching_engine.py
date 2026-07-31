"""
Unit tests for the ATS matching engine sub-modules and master engine.
"""

import pytest
from app.ai.matching.skill_matcher import calculate_skill_match
from app.ai.matching.experience_matcher import calculate_experience_match
from app.ai.matching.education_matcher import calculate_education_match
from app.ai.matching.semantic_matcher import calculate_semantic_match
from app.ai.matching.engine import compute_ats_score


def test_skill_matcher():
    required = ["Python", "FastAPI", "PostgreSQL", "Docker"]
    candidate = ["python", "fastapi", "docker", "react"]

    score, matched, missing = calculate_skill_match(required, candidate)
    assert score == 75.0  # 3 out of 4 matched
    assert "python" in matched
    assert "fastapi" in matched
    assert "postgresql" in missing


def test_experience_matcher():
    assert calculate_experience_match(required_years=3.0, candidate_years=5.0) == 100.0
    assert calculate_experience_match(required_years=4.0, candidate_years=2.0) == 50.0
    assert calculate_experience_match(required_years=0.0, candidate_years=1.0) == 100.0


def test_education_matcher():
    job_req = "Requires a Bachelor degree in Computer Science or related field."
    resume_text = "Master of Science in Software Engineering from Tech University."
    score = calculate_education_match(job_req, resume_text)
    assert score == 100.0  # Candidate Master >= required Bachelor


def test_compute_ats_score():
    job_data = {
        "title": "Senior Python Developer",
        "description": "Looking for a Senior Python Developer with FastAPI and Docker experience.",
        "required_skills": ["Python", "FastAPI", "Docker", "PostgreSQL"],
        "experience_years": 4,
    }
    resume_data = {
        "candidate_name": "Jane Developer",
        "years_of_experience": 5,
        "extracted_skills": ["python", "fastapi", "docker", "postgresql", "redis"],
    }
    resume_text = "Senior Python Engineer with 5 years experience building FastAPI and Docker microservices with PostgreSQL."

    result = compute_ats_score(
        job_data=job_data,
        resume_data=resume_data,
        resume_text=resume_text,
        job_description=job_data["description"],
    )

    assert result["overall_score"] > 80.0
    assert result["breakdown"]["skill_match"] == 100.0
    assert result["breakdown"]["experience_match"] == 100.0
    assert len(result["matched_skills"]) == 4
    assert len(result["missing_skills"]) == 0
