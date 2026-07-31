"""
Education Matcher Sub-Module (Weight: 10%).
Evaluates candidate education text against job requirements.
"""

import re

EDU_RANKING = {
    "phd": 4,
    "doctorate": 4,
    "master": 3,
    "ms": 3,
    "m.s.": 3,
    "mtech": 3,
    "mba": 3,
    "bachelor": 2,
    "bs": 2,
    "b.s.": 2,
    "btech": 2,
    "be": 2,
    "associate": 1,
}


def calculate_education_match(job_req_text: str, candidate_resume_text: str) -> float:
    """
    Calculate education match score (0.0 to 100.0).
    """
    if not job_req_text:
        return 100.0

    job_text = job_req_text.lower()
    cand_text = candidate_resume_text.lower()

    job_rank = 0
    for keyword, rank in EDU_RANKING.items():
        if re.search(r"\b" + re.escape(keyword) + r"\b", job_text):
            job_rank = max(job_rank, rank)

    if job_rank == 0:
        return 100.0  # No specific degree required

    cand_rank = 0
    for keyword, rank in EDU_RANKING.items():
        if re.search(r"\b" + re.escape(keyword) + r"\b", cand_text):
            cand_rank = max(cand_rank, rank)

    if cand_rank >= job_rank:
        return 100.0
    elif cand_rank > 0:
        return round((cand_rank / job_rank) * 80.0, 2)
    else:
        return 50.0  # Base credit if resume text present but degree title not parsed
