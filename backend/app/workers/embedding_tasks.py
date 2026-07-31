"""
Celery background tasks for async embedding generation and vector indexing.
"""

import asyncio
import uuid
import structlog

from app.workers.celery_app import celery_app
from app.ai.embeddings.encoder import generate_embedding
from app.ai.embeddings.faiss_store import faiss_vector_store
from app.database.engine import AsyncSessionLocal
from app.repositories.resume_repository import ResumeRepository

logger = structlog.get_logger(__name__)


async def _async_generate_and_store_embedding(resume_id_str: str):
    """Internal async task runner to generate vector embedding and update DB & FAISS."""
    resume_id = uuid.UUID(resume_id_str)
    async with AsyncSessionLocal() as session:
        repo = ResumeRepository(session)
        resume = await repo.get_by_id(resume_id)

        if not resume:
            logger.error("Resume not found for embedding task", resume_id=resume_id_str)
            return

        text_to_encode = resume.parsed_text or ""
        if not text_to_encode and resume.parsed_data:
            # Construct summary string if parsed_text missing
            skills = ", ".join(resume.parsed_data.get("extracted_skills", []))
            text_to_encode = f"Resume skills: {skills}"

        if not text_to_encode:
            logger.warning("No text available to encode embedding", resume_id=resume_id_str)
            return

        # 1. Generate 384-dim BGE vector
        vector = generate_embedding(text_to_encode)

        # 2. Update FAISS vector index
        faiss_vector_store.add_vector(resume_id_str, vector)

        # 3. Update DB record
        await repo.update_parsed_data(
            resume_id=resume_id,
            parsed_text=resume.parsed_text or "",
            parsed_data=resume.parsed_data or {},
            embedding=vector,
        )
        await session.commit()

        logger.info("Resume embedding generated and indexed successfully", resume_id=resume_id_str)


@celery_app.task(name="generate_resume_embedding")
def generate_resume_embedding_task(resume_id_str: str):
    """
    Celery task wrapper for generating resume embedding in background.
    """
    logger.info("Starting background task: generate_resume_embedding", resume_id=resume_id_str)
    asyncio.run(_async_generate_and_store_embedding(resume_id_str))
