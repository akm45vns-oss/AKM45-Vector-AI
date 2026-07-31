"""
Matching API Router — endpoints for running the ATS matching engine, candidate ranking, and semantic candidate search.
"""

import uuid
from typing import List

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.core.dependencies import DBSession, RecruiterUser, CurrentUser
from app.models.application import Application
from app.models.job import Job
from app.models.resume import Resume
from app.repositories.job_repository import JobRepository
from app.repositories.resume_repository import ResumeRepository
from app.schemas.matching import (
    CandidateRankItem,
    CandidateRankingResponse,
    MatchCalculateRequest,
    MatchResponse,
    SemanticSearchRequest,
    SemanticSearchResultItem,
)
from app.ai.matching.engine import compute_ats_score
from app.ai.embeddings.encoder import generate_embedding
from app.ai.embeddings.faiss_store import faiss_vector_store

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post(
    "/calculate",
    response_model=MatchResponse,
    summary="Calculate ATS match score between a job and a resume",
)
async def calculate_match(
    payload: MatchCalculateRequest,
    db: DBSession,
    current_user: CurrentUser,
) -> MatchResponse:
    """
    Run full ATS matching engine between a Job posting and a Resume.
    Calculates weighted score (Skill 40%, Semantic 30%, Experience 20%, Education 10%).
    """
    job_repo = JobRepository(db)
    resume_repo = ResumeRepository(db)

    job = await job_repo.get_by_id(payload.job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found.")

    resume = await resume_repo.get_by_id(payload.resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    job_dict = {
        "title": job.title,
        "description": job.description,
        "required_skills": job.required_skills or [],
        "experience_years": job.experience or 0,
    }

    resume_dict = resume.parsed_data or {}
    result = compute_ats_score(
        job_data=job_dict,
        resume_data=resume_dict,
        resume_text=resume.parsed_text or "",
        job_description=job.description,
        resume_embedding=resume.embedding,
    )

    return MatchResponse(
        job_id=job.id,
        resume_id=resume.id,
        overall_score=result["overall_score"],
        breakdown=result["breakdown"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
    )


@router.get(
    "/candidate-ranking/{job_id}",
    response_model=CandidateRankingResponse,
    summary="Get ranked candidates for a specific job posting",
)
async def get_candidate_ranking(
    job_id: uuid.UUID,
    db: DBSession,
    current_user: RecruiterUser,
) -> CandidateRankingResponse:
    """
    Retrieve ranked list of all candidates who applied for a job, sorted by ATS match score.
    """
    job_repo = JobRepository(db)
    job = await job_repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found.")

    # Fetch all applications for job
    result = await db.execute(
        select(Application, Resume)
        .join(Resume, Application.resume_id == Resume.id)
        .where(Application.job_id == job_id)
        .order_by(Application.match_score.desc())
    )
    rows = result.all()

    rankings: List[CandidateRankItem] = []
    job_dict = {
        "title": job.title,
        "description": job.description,
        "required_skills": job.required_skills or [],
        "experience_years": job.experience or 0,
    }

    for app, resume in rows:
        match_result = compute_ats_score(
            job_data=job_dict,
            resume_data=resume.parsed_data or {},
            resume_text=resume.parsed_text or "",
            job_description=job.description,
            resume_embedding=resume.embedding,
        )

        cand_name = (resume.parsed_data or {}).get("candidate_name", f"Candidate {str(resume.user_id)[:8]}")

        rankings.append(
            CandidateRankItem(
                application_id=app.id,
                candidate_id=resume.user_id,
                candidate_name=cand_name,
                resume_id=resume.id,
                match_score=app.match_score if app.match_score is not None else match_result["overall_score"],
                breakdown=match_result["breakdown"],
                matched_skills=match_result["matched_skills"],
                missing_skills=match_result["missing_skills"],
                status=app.status.value if hasattr(app.status, "value") else str(app.status),
            )
        )

    # Sort descending by match_score
    rankings.sort(key=lambda x: x.match_score, reverse=True)

    return CandidateRankingResponse(
        job_id=job_id,
        total_candidates=len(rankings),
        rankings=rankings,
    )


@router.post(
    "/search",
    response_model=List[SemanticSearchResultItem],
    summary="Semantic candidate search across vector database",
)
async def semantic_search(
    payload: SemanticSearchRequest,
    db: DBSession,
    current_user: RecruiterUser,
) -> List[SemanticSearchResultItem]:
    """
    Search candidate resumes semantically using natural language query via FAISS vector store.
    """
    query_vector = generate_embedding(payload.query)
    results = faiss_vector_store.search(query_vector, top_k=payload.top_k)

    search_items: List[SemanticSearchResultItem] = []
    resume_repo = ResumeRepository(db)

    for resume_id_str, similarity_score in results:
        try:
            r_uuid = uuid.UUID(resume_id_str)
            resume = await resume_repo.get_by_id(r_uuid)
            if resume:
                cand_name = (resume.parsed_data or {}).get("candidate_name", "Unknown Candidate")
                skills = (resume.parsed_data or {}).get("extracted_skills", [])
                search_items.append(
                    SemanticSearchResultItem(
                        resume_id=resume.id,
                        candidate_name=cand_name,
                        similarity_score=round(similarity_score * 100.0, 2),
                        matched_skills=skills,
                    )
                )
        except ValueError:
            continue

    return search_items
