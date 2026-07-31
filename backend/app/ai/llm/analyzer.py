"""
Master LLM Candidate Analyzer module.
Executes candidate evaluation via Ollama LLM with intelligent heuristic fallback if LLM service is offline.
"""

from typing import Any, Dict, List
import structlog

from app.ai.llm.ollama_client import ollama_client
from app.ai.llm.prompts import SYSTEM_PROMPT_EVALUATOR, build_candidate_analysis_prompt

logger = structlog.get_logger(__name__)


async def generate_candidate_llm_feedback(
    job_title: str,
    job_description: str,
    required_skills: List[str],
    candidate_name: str,
    candidate_resume_text: str,
    matched_skills: List[str],
    missing_skills: List[str],
    ats_score: float,
) -> Dict[str, Any]:
    """
    Generate comprehensive AI feedback for a candidate application using LLM.
    Includes rule-based fallback if Ollama server is unreachable.
    """
    prompt = build_candidate_analysis_prompt(
        job_title=job_title,
        job_description=job_description,
        required_skills=required_skills,
        candidate_name=candidate_name,
        candidate_resume_text=candidate_resume_text,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        ats_score=ats_score,
    )

    llm_result = await ollama_client.generate_json(prompt, system_prompt=SYSTEM_PROMPT_EVALUATOR)

    if llm_result and isinstance(llm_result, dict) and "hiring_recommendation" in llm_result:
        logger.info("LLM evaluation generated via Ollama successfully")
        return llm_result

    logger.warning("Ollama LLM response unavailable, generating heuristic evaluation fallback")
    return _generate_fallback_feedback(
        job_title=job_title,
        candidate_name=candidate_name,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        ats_score=ats_score,
    )


def _generate_fallback_feedback(
    job_title: str,
    candidate_name: str,
    matched_skills: List[str],
    missing_skills: List[str],
    ats_score: float,
) -> Dict[str, Any]:
    """Rule-based fallback evaluation report when Ollama service is unavailable."""
    if ats_score >= 80.0:
        recommendation = "Strong Hire"
        reasoning = f"{candidate_name} exhibits excellent skill alignment ({ats_score}% ATS score) for {job_title}."
    elif ats_score >= 65.0:
        recommendation = "Hire"
        reasoning = f"{candidate_name} possesses core required skills with an ATS score of {ats_score}%."
    elif ats_score >= 45.0:
        recommendation = "Possible Fit"
        reasoning = f"Moderate match ({ats_score}% score). Candidate has key skills but is missing {len(missing_skills)} required items."
    else:
        recommendation = "Do Not Pursue"
        reasoning = f"Low skill overlap ({ats_score}% score). Key required technologies are absent from resume."

    return {
        "candidate_summary": f"{candidate_name} applied for {job_title} with an ATS score of {ats_score}%. Matched {len(matched_skills)} skills.",
        "strengths": [f"Demonstrated proficiency in {s}" for s in matched_skills[:3]] or ["Relevant background in target domain"],
        "weaknesses": [f"Lacks proven experience in {s}" for s in missing_skills[:2]] or ["Minor experience gaps"],
        "missing_critical_skills": missing_skills,
        "interview_questions": [
            f"Can you describe your practical experience using {matched_skills[0] if matched_skills else 'core stack'} in production?",
            f"How quickly can you get up to speed with {missing_skills[0] if missing_skills else 'new tools'}?",
            "Tell me about a complex project technical challenge you resolved recently.",
        ],
        "hiring_recommendation": recommendation,
        "recommendation_reasoning": reasoning,
    }
