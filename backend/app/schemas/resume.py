"""
Pydantic schemas for Resume API requests and responses.
"""

import uuid
from datetime import datetime
from typing import Optional, Any, Dict, List

from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    """Returned immediately after resume file is uploaded."""
    id: uuid.UUID
    user_id: uuid.UUID
    file_name: str
    file_url: str
    file_size: int
    file_type: str
    status: str = "uploaded"
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeDetailResponse(BaseModel):
    """Full detail response for parsed resume."""
    id: uuid.UUID
    user_id: uuid.UUID
    file_name: str
    file_url: str
    file_size: int
    file_type: str
    parsed_text: Optional[str] = None
    parsed_data: Dict[str, Any] = Field(default_factory=dict)
    ats_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResumeListResponse(BaseModel):
    """Paginated list of user resumes."""
    items: List[ResumeUploadResponse]
    total: int
