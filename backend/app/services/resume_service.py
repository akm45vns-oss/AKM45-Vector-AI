"""
Resume service — handles uploading, storage, parsing triggers, and retrieval.
"""

import uuid
from typing import Optional, Sequence

import structlog
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.resume_repository import ResumeRepository
from app.schemas.resume import ResumeDetailResponse, ResumeUploadResponse
from app.utils.file_validation import validate_resume_file, validate_file_size
from app.utils.storage import storage_manager

logger = structlog.get_logger(__name__)


class ResumeService:
    """Service layer for resume file handling and management."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = ResumeRepository(db)

    async def upload_resume(self, file: UploadFile, current_user: User) -> ResumeUploadResponse:
        """
        Validate, save to disk, and persist Resume record.
        """
        # Validate filename & ext
        orig_filename, ext = validate_resume_file(file)

        # Validate file size
        file_size = await validate_file_size(file)

        # Save to local storage
        stored_name, file_url, abs_path = await storage_manager.save_file(
            file, filename_prefix=str(current_user.id)[:8]
        )

        # Extract text based on file type
        raw_text = ""
        try:
            if ext == "pdf":
                from app.ai.parser.pdf_parser import extract_text_from_pdf
                raw_text = extract_text_from_pdf(abs_path)
            elif ext == "docx":
                from app.ai.parser.docx_parser import extract_text_from_docx
                raw_text = extract_text_from_docx(abs_path)
        except Exception as e:
            logger.error("Text extraction failed during upload", error=str(e))

        # Parse entities & skills
        parsed_data = {}
        if raw_text:
            try:
                from app.ai.parser.extractor import parse_resume_content
                parsed_data = parse_resume_content(raw_text)
            except Exception as e:
                logger.error("Resume entity parsing failed during upload", error=str(e))

        # Persist DB record
        resume = await self._repo.create(
            user_id=current_user.id,
            file_url=file_url,
            file_name=orig_filename,
            file_size=file_size,
            file_type=ext.upper(),
            parsed_text=raw_text,
            parsed_data=parsed_data,
        )

        logger.info(
            "Resume uploaded and parsed successfully",
            resume_id=str(resume.id),
            user_id=str(current_user.id),
            file_size=file_size,
            skills_count=len(parsed_data.get("extracted_skills", [])),
        )

        return ResumeUploadResponse.model_validate(resume)

    async def get_resume(self, resume_id: uuid.UUID, current_user: User) -> ResumeDetailResponse:
        """Retrieve resume by ID with authorization check."""
        resume = await self._repo.get_by_id(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found.",
            )

        # Authorization check: candidates can only view their own; recruiters/admins can view any
        if current_user.role == "candidate" and resume.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this resume.",
            )

        return ResumeDetailResponse.model_validate(resume)

    async def list_user_resumes(
        self, current_user: User, limit: int = 20, offset: int = 0
    ) -> Sequence[ResumeUploadResponse]:
        """List all resumes uploaded by current user."""
        resumes = await self._repo.list_by_user(current_user.id, limit=limit, offset=offset)
        return [ResumeUploadResponse.model_validate(r) for r in resumes]

    async def delete_resume(self, resume_id: uuid.UUID, current_user: User) -> bool:
        """Delete resume record and associated file."""
        resume = await self._repo.get_by_id(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found.",
            )

        if current_user.role == "candidate" and resume.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this resume.",
            )

        # Remove file from storage
        await storage_manager.delete_file(resume.file_url)

        # Remove record
        deleted = await self._repo.delete(resume_id)
        logger.info("Resume deleted", resume_id=str(resume_id))
        return deleted
