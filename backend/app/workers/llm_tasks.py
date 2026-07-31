"""
Celery background task for async LLM candidate evaluation.
"""

import asyncio
import uuid
import structlog
from sqlalchemy import select

from app.workers.celery_app import celery_app
from app.database.engine import AsyncSessionLocal
from app.models.application import Application
from app.models.job import Job
from app.models.resume import Resume
from app.ai.matching.engine import compute_ats_score
from app.ai.llm.analyzer import generate_candidate_llm_feedback

logger = structlog.get_logger(__name__)


async def _async_generate_llm_analysis(application_id_str: str):
    """Internal runner to execute LLM feedback generation and update Application record in DB."""
    app_id = uuid.UUID(application_id_str)
    async with AsyncSessionLocal() as session:
        # Fetch application with Job and Resume
        result = await session.execute(
            select(Application, Job, Resume)
            .join(Job, Application.job_id == Job.id)
            .join(Resume, Application.resume_id == Resume.id)
            .where(Application.id == app_id)
        )
        row = result.first()
        if not row:
            logger.error("Application not found for LLM task", application_id=application_id_str)
            return

        application, job, resume = row

        job_dict = {
            "title": job.title,
            "description": job.description,
            "required_skills": job.required_skills or [],
            "experience_years": job.experience or 0,
        }

        match_result = compute_ats_score(
            job_data=job_dict,
            resume_data=resume.parsed_data or {},
            resume_text=resume.parsed_text or "",
            job_description=job.description,
            resume_embedding=resume.embedding,
        )

        cand_name = (resume.parsed_data or {}).get("candidate_name", "Candidate")

        # Generate LLM analysis report
        llm_feedback = await generate_candidate_llm_feedback(
            job_title=job.title,
            job_description=job.description,
            required_skills=job.required_skills or [],
            candidate_name=cand_name,
            candidate_resume_text=resume.parsed_text or "",
            matched_skills=match_result["matched_skills"],
            missing_skills=match_result["missing_skills"],
            ats_score=match_result["overall_score"],
        )

        # Update application match_score and feedback JSON
        application.match_score = match_result["overall_score"]
        application.feedback = llm_feedback
        await session.commit()

        logger.info("Application LLM feedback updated", application_id=application_id_str, match_score=application.match_score)


@celery_app.task(name="generate_llm_analysis")
def generate_llm_analysis_task(application_id_str: str):
    """
    Celery task wrapper for candidate LLM analysis.
    """
    logger.info("Starting Celery task: generate_llm_analysis", application_id=application_id_str)
    asyncio.run(_async_generate_llm_analysis(application_id_str))
