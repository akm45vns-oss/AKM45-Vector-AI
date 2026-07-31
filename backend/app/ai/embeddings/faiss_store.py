"""
FAISS Vector Store wrapper.
Uses IndexFlatIP (Inner Product) for normalized vectors (cosine similarity).
Maps UUID strings to index offsets using an internal ID mapping dict.
"""

import os
import pickle
from typing import List, Tuple, Dict
import faiss
import numpy as np
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)


class FAISSVectorStore:
    """FAISS vector database wrapper with index persistence and ID mapping."""

    def __init__(self, dimension: int = 384, index_path: str = settings.FAISS_INDEX_PATH) -> None:
        self.dimension = dimension
        self.index_path = index_path
        self.index_file = f"{index_path}.index"
        self.mapping_file = f"{index_path}.pkl"

        # IndexFlatIP uses Inner Product (equivalent to Cosine Similarity when vectors are L2-normalized)
        self.index = faiss.IndexFlatIP(dimension)
        self.id_to_uuid: Dict[int, str] = {}
        self.uuid_to_id: Dict[str, int] = {}
        self._next_id = 0

        self.load()

    def add_vector(self, entity_id: str, vector: List[float]) -> int:
        """
        Add or update a vector embedding for an entity (resume or job ID).
        """
        vec_np = np.array([vector], dtype=np.float32)
        faiss.normalize_L2(vec_np)

        if entity_id in self.uuid_to_id:
            # Overwrite scenario: for simple IndexFlat, append new and update map
            faiss_id = self.uuid_to_id[entity_id]
        else:
            faiss_id = self._next_id
            self._next_id += 1

        self.id_to_uuid[faiss_id] = entity_id
        self.uuid_to_id[entity_id] = faiss_id

        self.index.add(vec_np)
        self.save()
        logger.info("Added vector to FAISS store", entity_id=entity_id, faiss_id=faiss_id, total_vectors=self.index.ntotal)
        return faiss_id

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for top_k most similar vectors.

        Returns:
            List of (entity_id, similarity_score)
        """
        if self.index.ntotal == 0:
            return []

        query_np = np.array([query_vector], dtype=np.float32)
        faiss.normalize_L2(query_np)

        k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_np, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx in self.id_to_uuid:
                entity_id = self.id_to_uuid[idx]
                results.append((entity_id, float(score)))

        return results

    def save((self) -> None:
        """Persist index and ID map to disk."""
        os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
        faiss.write_index(self.index, self.index_file)
        with open(self.mapping_file, "wb") as f:
            pickle.dump({"id_to_uuid": self.id_to_uuid, "uuid_to_id": self.uuid_to_id, "_next_id": self._next_id}, f)
        logger.info("Saved FAISS index to disk", path=self.index_file)

    def load(self) -> None:
        """Load index and ID map from disk if present."""
        if os.path.exists(self.index_file) and os.path.exists(self.mapping_file):
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.mapping_file, "rb") as f:
                    data = pickle.load(f)
                    self.id_to_uuid = data.get("id_to_uuid", {})
                    self.uuid_to_id = data.get("uuid_to_id", {})
                    self._next_id = data.get("_next_id", 0)
                logger.info("Loaded FAISS index from disk", total_vectors=self.index.ntotal)
            except Exception as e:
                logger.error("Failed to load FAISS index from disk", error=str(e))


faiss_vector_store = FAISSVectorStore()
