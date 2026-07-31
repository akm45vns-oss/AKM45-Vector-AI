"""
Experience Matcher Sub-Module (Weight: 20%).
Compares candidate years of experience against job required experience.
"""


def calculate_experience_match(
    required_years: float, candidate_years: float
) -> float:
    """
    Calculate experience match score (0.0 to 100.0).

    - If candidate has >= required_years: 100%
    - If required_years is 0: 100%
    - Proportional partial credit if below requirement.
    """
    if required_years <= 0:
        return 100.0

    if candidate_years >= required_years:
        return 100.0

    ratio = candidate_years / required_years
    score = ratio * 100.0
    return round(min(score, 100.0), 2)
