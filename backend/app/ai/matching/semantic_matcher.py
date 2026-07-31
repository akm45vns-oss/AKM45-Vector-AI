"""
Semantic Matcher Sub-Module (Weight: 30%).
Calculates vector cosine similarity between job description embedding and candidate resume embedding.
"""

from typing import List, Optional
import numpy as np
from app.ai.embeddings.encoder import generate_embedding


def calculate_semantic_match(
    job_description: str,
    candidate_text: str,
    resume_embedding: Optional[List[float]] = None,
    job_embedding: Optional[List[float]] = None,
) -> float:
    """
    Calculate semantic similarity score (0.0 to 100.0) between job and resume.
    Uses precomputed vector embeddings if available, otherwise generates them on-the-fly.
    """
    v_job = job_embedding or generate_embedding(job_description)
    v_cand = resume_embedding or generate_embedding(candidate_text)

    if not v_job or not v_cand:
        return 50.0

    vec_job = np.array(v_job, dtype=np.float32)
    vec_cand = np.array(v_cand, dtype=np.float32)

    # Cosine similarity for normalized vectors = dot product
    norm_job = np.linalg.norm(vec_job)
    norm_cand = np.linalg.norm(vec_cand)

    if norm_job == 0 or norm_cand == 0:
        return 50.0

    similarity = np.dot(vec_job, vec_cand) / (norm_job * norm_cand)
    
    # Scale cosine range [-1.0, 1.0] or [0.0, 1.0] to percentage score [0.0, 100.0]
    score = max(0.0, float(similarity)) * 100.0
    return round(score, 2)
