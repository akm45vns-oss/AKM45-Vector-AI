"""
File validation utilities for upload handling.
Validates file extension, MIME type, and size limits.
"""

from typing import Tuple
from fastapi import UploadFile, HTTPException, status

from app.core.config import settings

ALLOWED_EXTENSIONS = {"pdf", "docx"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
}


def validate_resume_file(file: UploadFile) -> Tuple[str, str]:
    """
    Validate an uploaded resume file.

    Returns:
        Tuple[filename, extension]

    Raises:
        HTTPException 400: If file type, extension, or size is invalid.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a filename.",
        )

    # Extension check
    filename = file.filename
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '.{ext}'. Supported formats: PDF, DOCX.",
        )

    # Content type check (allow fallback if client doesn't send header correctly)
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        # Some browsers send generic octet-stream for docx
        if file.content_type != "application/octet-stream":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported MIME type '{file.content_type}'. Supported: PDF, DOCX.",
            )

    return filename, ext


async def validate_file_size(file: UploadFile) -> int:
    """
    Validate that the file size is within configured limits.
    Reads file content to measure byte length, then resets seek offset.
    """
    contents = await file.read()
    size_bytes = len(contents)
    await file.seek(0)

    if size_bytes == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if size_bytes > settings.MAX_FILE_SIZE_BYTES:
        max_mb = settings.MAX_FILE_SIZE_MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of {max_mb}MB.",
        )

    return size_bytes
