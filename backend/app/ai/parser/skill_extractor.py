"""
Skill extraction engine using spaCy, phrase matching, and regex boundary detection.
"""

import re
from typing import Dict, List, Set
import spacy
from spacy.matcher import PhraseMatcher
import structlog

from app.ai.parser.skills_dict import SKILL_TAXONOMY, ALL_SKILLS_SET

logger = structlog.get_logger(__name__)

# Load small English model lazily
_nlp = None


def get_nlp_model():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except Exception:
            # Fallback to blank model if en_core_web_sm is not pre-installed
            _nlp = spacy.blank("en")
    return _nlp


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract skills from text categorized by skill category.

    Returns:
        Dict[category_name, List[found_skills]]
    """
    if not text:
        return {cat: [] for cat in SKILL_TAXONOMY}

    text_lower = text.lower()
    found_skills_by_category: Dict[str, Set[str]] = {cat: set() for cat in SKILL_TAXONOMY}

    # 1. Regex boundary matching for skills (prevents 'c' matching inside 'cat')
    for category, skills_list in SKILL_TAXONOMY.items():
        for skill in skills_list:
            # Escape skill name for regex
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                found_skills_by_category[category].add(skill)

    # Convert sets to sorted lists
    result = {cat: sorted(list(skills)) for cat, skills in found_skills_by_category.items()}

    # Calculate total unique skills
    total_unique = len({skill for cat in result.values() for skill in cat})
    logger.info("Skill extraction complete", total_skills_found=total_unique)

    return result
