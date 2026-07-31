"""
Resume API Router — endpoints for uploading, retrieving, listing, and deleting resumes.
"""

import uuid
from typing import List

import structlog
from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse
import os

from app.core.dependencies import CurrentVerifiedUser, DBSession, CurrentUser
from app.schemas.auth import MessageResponse
from app.schemas.resume import (
    ResumeDetailResponse,
    ResumeListResponse,
    ResumeUploadResponse,
)
from app.services.resume_service import ResumeService
from app.utils.storage import storage_manager

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a resume (PDF or DOCX)",
)
async def upload_resume(
    db: DBSession,
    current_user: CurrentVerifiedUser,
    file: UploadFile = File(...),
) -> ResumeUploadResponse:
    """
    Upload a candidate resume file.

    - Accepts PDF or DOCX format.
    - Validates size (max 10MB).
    - Saves file locally and creates DB record.
    """
    service = ResumeService(db)
    return await service.upload_resume(file, current_user)


@router.get(
    "/my-resumes",
    response_model=List[ResumeUploadResponse],
    summary="List current user's uploaded resumes",
)
async def list_my_resumes(
    db: DBSession,
    current_user: CurrentUser,
    limit: int = 20,
    offset: int = 0,
) -> List[ResumeUploadResponse]:
    """Retrieve list of all resumes uploaded by the current user."""
    service = ResumeService(db)
    return await service.list_user_resumes(current_user, limit=limit, offset=offset)


@router.get(
    "/{id}",
    response_model=ResumeDetailResponse,
    summary="Get resume details and parsed data by ID",
)
async def get_resume(
    id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> ResumeDetailResponse:
    """Get parsed resume details by ID."""
    service = ResumeService(db)
    return await service.get_resume(id, current_user)


@router.get(
    "/{id}/file",
    summary="Download or stream the original uploaded resume file",
)
async def download_resume_file(
    id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
):
    """Download/stream original resume document file."""
    service = ResumeService(db)
    resume = await service.get_resume(id, current_user)
    abs_path = storage_manager.get_absolute_path(resume.file_url)

    if not os.path.exists(abs_path):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File content not found on server storage.",
        )

    media_type = "application/pdf" if resume.file_type.lower() == "pdf" else "application/octet-stream"
    return FileResponse(
        path=abs_path,
        filename=resume.file_name,
        media_type=media_type,
    )


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    summary="Delete a resume",
)
async def delete_resume(
    id: uuid.UUID,
    db: DBSession,
    current_user: CurrentUser,
) -> MessageResponse:
    """Delete resume record and remove file from storage."""
    service = ResumeService(db)
    await service.delete_resume(id, current_user)
    return MessageResponse(message="Resume deleted successfully.")
