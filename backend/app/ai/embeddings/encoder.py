"""
Text embedding encoder using SentenceTransformers.
Model: BAAI/bge-small-en-v1.5 (384 dimensions, fast & accurate embedding model).
"""

from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

_model: Union[SentenceTransformer, None] = None


def get_embedding_model() -> SentenceTransformer:
    """Lazy load the SentenceTransformer embedding model."""
    global _model
    if _model is None:
        logger.info("Loading embedding model", model_name=settings.HF_EMBEDDING_MODEL)
        _model = SentenceTransformer(
            settings.HF_EMBEDDING_MODEL,
            cache_folder=settings.HF_CACHE_DIR
        )
    return _model


def generate_embedding(text: str) -> List[float]:
    """
    Generate a 384-dimensional normalized vector embedding for input text.
    L2 normalized so inner product equals cosine similarity.
    """
    if not text or not text.strip():
        return [0.0] * 384

    model = get_embedding_model()
    # BGE models work best with query/passage prefixing if needed, but standard encode is robust
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate normalized vector embeddings for a list of texts."""
    if not texts:
        return []

    model = get_embedding_model()
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return embeddings.tolist()
