"""
Pydantic schemas for Matching API endpoints.
"""

import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class MatchCalculateRequest(BaseModel):
    """Request body to trigger match calculation between a job and a resume."""
    job_id: uuid.UUID
    resume_id: uuid.UUID


class MatchBreakdown(BaseModel):
    skill_match: float
    semantic_match: float
    experience_match: float
    education_match: float


class MatchResponse(BaseModel):
    """Result of ATS match calculation."""
    job_id: uuid.UUID
    resume_id: uuid.UUID
    overall_score: float
    breakdown: MatchBreakdown
    matched_skills: List[str]
    missing_skills: List[str]


class CandidateRankItem(BaseModel):
    """Ranked candidate item in ranking list."""
    application_id: Optional[uuid.UUID] = None
    candidate_id: uuid.UUID
    candidate_name: str
    resume_id: uuid.UUID
    match_score: float
    breakdown: MatchBreakdown
    matched_skills: List[str]
    missing_skills: List[str]
    status: str = "applied"


class CandidateRankingResponse(BaseModel):
    job_id: uuid.UUID
    total_candidates: int
    rankings: List[CandidateRankItem]


class SemanticSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, examples=["Senior Python Engineer with FastAPI"])
    top_k: int = Field(default=10, ge=1, le=50)


class SemanticSearchResultItem(BaseModel):
    resume_id: uuid.UUID
    candidate_name: Optional[str] = None
    similarity_score: float
    matched_skills: List[str]
