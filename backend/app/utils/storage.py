"""
Local disk storage manager.
Handles saving, reading, and deleting uploaded files.
Abstracted interface so it can be swapped with Supabase/S3 in production.
"""

import os
import uuid
import aiofiles
import structlog
from fastapi import UploadFile

from app.core.config import settings

logger = structlog.get_logger(__name__)


class StorageManager:
    """Manages file persistence to local disk."""

    def __init__(self, upload_dir: str = settings.UPLOAD_DIR) -> None:
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_file(self, file: UploadFile, filename_prefix: str = "") -> Tuple_Save_Result:
        """
        Save an UploadFile asynchronously to disk with a unique UUID filename.

        Returns:
            tuple of (saved_filename, relative_file_url, absolute_path)
        """
        ext = file.filename.split(".")[-1].lower() if file.filename and "." in file.filename else "file"
        unique_name = f"{filename_prefix}_{uuid.uuid4().hex}.{ext}" if filename_prefix else f"{uuid.uuid4().hex}.{ext}"
        abs_path = os.path.join(self.upload_dir, unique_name)

        async with aiofiles.open(abs_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
            await file.seek(0)

        file_url = f"/uploads/{unique_name}"
        logger.info("File saved to storage", path=abs_path, url=file_url)
        return unique_name, file_url, abs_path

    async def delete_file(self, file_url_or_name: str) -> bool:
        """Delete a file from disk by filename or URL path."""
        filename = os.path.basename(file_url_or_name)
        abs_path = os.path.join(self.upload_dir, filename)

        if os.path.exists(abs_path):
            try:
                os.remove(abs_path)
                logger.info("File deleted from storage", path=abs_path)
                return True
            except OSError as e:
                logger.error("Failed to delete file from storage", path=abs_path, error=str(e))
                return False
        return False

    def get_absolute_path(self, file_url_or_name: str) -> str:
        """Get absolute path on disk for a given filename or URL."""
        filename = os.path.basename(file_url_or_name)
        return os.path.join(self.upload_dir, filename)


# Typed return helper
from typing import NamedTuple

class Tuple_Save_Result(NamedTuple):
    stored_filename: str
    file_url: str
    absolute_path: str


storage_manager = StorageManager()
