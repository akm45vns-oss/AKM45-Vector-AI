"""
Master ATS Matching Engine.
Aggregates sub-scores using weighted formula:
  - Skill Match: 40%
  - Semantic Match: 30%
  - Experience Match: 20%
  - Education Match: 10%
"""

from typing import Any, Dict, List, Optional
import structlog

from app.ai.matching.skill_matcher import calculate_skill_match
from app.ai.matching.experience_matcher import calculate_experience_match
from app.ai.matching.education_matcher import calculate_education_match
from app.ai.matching.semantic_matcher import calculate_semantic_match

logger = structlog.get_logger(__name__)

# Default weights as specified in prompt architecture
WEIGHT_SKILL = 0.40
WEIGHT_SEMANTIC = 0.30
WEIGHT_EXPERIENCE = 0.20
WEIGHT_EDUCATION = 0.10


def compute_ats_score(
    job_data: Dict[str, Any],
    resume_data: Dict[str, Any],
    resume_text: str = "",
    job_description: str = "",
    resume_embedding: Optional[List[float]] = None,
    job_embedding: Optional[List[float]] = None,
) -> Dict[str, Any]:
    """
    Calculate full ATS match breakdown and final overall score.

    Returns:
        Dict containing:
          - overall_score (0.0 to 100.0)
          - breakdown: { skill_score, semantic_score, experience_score, education_score }
          - matched_skills: List[str]
          - missing_skills: List[str]
    """
    req_skills = job_data.get("required_skills", [])
    cand_skills = resume_data.get("extracted_skills", [])

    # 1. Skill Match (40%)
    skill_score, matched_skills, missing_skills = calculate_skill_match(req_skills, cand_skills)

    # 2. Semantic Match (30%)
    job_desc = job_description or job_data.get("description", "")
    sem_score = calculate_semantic_match(
        job_description=job_desc,
        candidate_text=resume_text,
        resume_embedding=resume_embedding,
        job_embedding=job_embedding,
    )

    # 3. Experience Match (20%)
    req_exp = float(job_data.get("experience_years", 0) or job_data.get("experience", 0) or 0)
    cand_exp = float(resume_data.get("years_of_experience", 0) or 0)
    exp_score = calculate_experience_match(req_exp, cand_exp)

    # 4. Education Match (10%)
    edu_score = calculate_education_match(
        job_req_text=job_desc,
        candidate_resume_text=resume_text,
    )

    # Calculate weighted overall ATS score
    overall_score = (
        (skill_score * WEIGHT_SKILL)
        + (sem_score * WEIGHT_SEMANTIC)
        + (exp_score * WEIGHT_EXPERIENCE)
        + (edu_score * WEIGHT_EDUCATION)
    )
    overall_score = round(overall_score, 2)

    logger.info("ATS score computed", overall_score=overall_score, skill_score=skill_score, sem_score=sem_score)

    return {
        "overall_score": overall_score,
        "breakdown": {
            "skill_match": skill_score,
            "semantic_match": sem_score,
            "experience_match": exp_score,
            "education_match": edu_score,
        },
        "weights": {
            "skill": WEIGHT_SKILL,
            "semantic": WEIGHT_SEMANTIC,
            "experience": WEIGHT_EXPERIENCE,
            "education": WEIGHT_EDUCATION,
        },
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }
