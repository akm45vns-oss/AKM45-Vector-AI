"""
Resume repository — data access operations for the Resume model.
"""

import uuid
from typing import Optional, Sequence

import structlog
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume

logger = structlog.get_logger(__name__)


class ResumeRepository:
    """Data access layer for Resume model."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, resume_id: uuid.UUID) -> Optional[Resume]:
        """Fetch resume by UUID."""
        result = await self._db.execute(
            select(Resume).where(Resume.id == resume_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self, user_id: uuid.UUID, limit: int = 20, offset: int = 0
    ) -> Sequence[Resume]:
        """List resumes uploaded by a specific candidate user."""
        result = await self._db.execute(
            select(Resume)
            .where(Resume.user_id == user_id)
            .order_by(Resume.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        file_url: str,
        file_name: str,
        file_size: int,
        file_type: str,
        parsed_text: Optional[str] = None,
        parsed_data: Optional[dict] = None,
        ats_score: Optional[float] = None,
    ) -> Resume:
        """Create and store a new resume record."""
        resume = Resume(
            user_id=user_id,
            file_url=file_url,
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            parsed_text=parsed_text,
            parsed_data=parsed_data or {},
            ats_score=ats_score,
        )
        self._db.add(resume)
        await self._db.flush()
        await self._db.refresh(resume)
        logger.info("Resume record created", resume_id=str(resume.id), user_id=str(user_id))
        return resume

    async def update_parsed_data(
        self,
        resume_id: uuid.UUID,
        parsed_text: str,
        parsed_data: dict,
        ats_score: Optional[float] = None,
        embedding: Optional[list[float]] = None,
    ) -> Optional[Resume]:
        """Update parsed text, parsed structured JSON, and vector embedding."""
        values: dict = {
            "parsed_text": parsed_text,
            "parsed_data": parsed_data,
        }
        if ats_score is not None:
            values["ats_score"] = ats_score
        if embedding is not None:
            values["embedding"] = embedding

        await self._db.execute(
            update(Resume).where(Resume.id == resume_id).values(**values)
        )
        return await self.get_by_id(resume_id)

    async def delete(self, resume_id: uuid.UUID) -> bool:
        """Delete resume record by ID."""
        result = await self._db.execute(
            delete(Resume).where(Resume.id == resume_id)
        )
        return result.rowcount > 0
