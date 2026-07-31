"""
Skill Matcher Sub-Module (Weight: 40%).
Calculates matching score between job required skills and candidate extracted skills.
Returns match percentage and list of missing skills.
"""

from typing import List, Set, Tuple, Dict


def calculate_skill_match(
    required_skills: List[str], candidate_skills: List[str]
) -> Tuple[float, List[str], List[str]]:
    """
    Calculate skill match score (0.0 to 100.0).

    Returns:
        Tuple[score, matched_skills, missing_skills]
    """
    if not required_skills:
        return 100.0, candidate_skills, []

    req_set: Set[str] = {s.lower().strip() for s in required_skills if s.strip()}
    cand_set: Set[str] = {s.lower().strip() for s in candidate_skills if s.strip()}

    if not req_set:
        return 100.0, candidate_skills, []

    matched = req_set.intersection(cand_set)
    missing = req_set - cand_set

    # Overlap score
    score = (len(matched) / len(req_set)) * 100.0

    return round(score, 2), sorted(list(matched)), sorted(list(missing))
