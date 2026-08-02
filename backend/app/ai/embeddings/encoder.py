"""
Text embedding encoder using SentenceTransformers.
Model: BAAI/bge-small-en-v1.5 (384 dimensions, fast & accurate embedding model).
"""

from typing import Any, List, Union
import numpy as np
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

_model: Any = None


def get_embedding_model() -> Any:
    """Lazy load the SentenceTransformer embedding model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading embedding model", model_name=settings.HF_EMBEDDING_MODEL)
            _model = SentenceTransformer(
                settings.HF_EMBEDDING_MODEL,
                cache_folder=settings.HF_CACHE_DIR
            )
        except ImportError:
            logger.warning("sentence_transformers package not installed. Embeddings will use dummy zero-vectors.")
            return None
    return _model


def generate_embedding(text: str) -> List[float]:
    """
    Generate a 384-dimensional normalized vector embedding for input text.
    L2 normalized so inner product equals cosine similarity.
    """
    if not text or not text.strip():
        return [0.0] * 384

    model = get_embedding_model()
    if model is None:
        return [0.0] * 384

    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate normalized vector embeddings for a list of texts."""
    if not texts:
        return []

    model = get_embedding_model()
    if model is None:
        return [[0.0] * 384 for _ in texts]

    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return embeddings.tolist()
