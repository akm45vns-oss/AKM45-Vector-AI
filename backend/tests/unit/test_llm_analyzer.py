"""
Unit tests for LLM Candidate Analyzer module and fallback engine.
"""

import pytest
from app.ai.llm.analyzer import _generate_fallback_feedback, generate_candidate_llm_feedback


def test_fallback_feedback_high_score():
    feedback = _generate_fallback_feedback(
        job_title="Senior Python Engineer",
        candidate_name="Jane Doe",
        matched_skills=["Python", "FastAPI", "Docker"],
        missing_skills=[],
        ats_score=92.5,
    )
    assert feedback["hiring_recommendation"] == "Strong Hire"
    assert len(feedback["strengths"]) == 3
    assert len(feedback["interview_questions"]) == 3


def test_fallback_feedback_low_score():
    feedback = _generate_fallback_feedback(
        job_title="DevOps Lead",
        candidate_name="John Smith",
        matched_skills=["Git"],
        missing_skills=["Kubernetes", "Terraform", "AWS"],
        ats_score=35.0,
    )
    assert feedback["hiring_recommendation"] == "Do Not Pursue"
    assert len(feedback["missing_critical_skills"]) == 3


@pytest.mark.asyncio
async def test_generate_candidate_llm_feedback_fallback():
    feedback = await generate_candidate_llm_feedback(
        job_title="Frontend Developer",
        job_description="React and Next.js expert needed.",
        required_skills=["React", "Next.js", "TypeScript"],
        candidate_name="Bob Developer",
        candidate_resume_text="React and Next.js developer with 4 years experience.",
        matched_skills=["React", "Next.js"],
        missing_skills=["TypeScript"],
        ats_score=75.0,
    )
    assert "hiring_recommendation" in feedback
    assert "interview_questions" in feedback
    assert len(feedback["interview_questions"]) == 3
