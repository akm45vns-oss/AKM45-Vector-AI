"""
Unit tests for embedding encoder and FAISS vector store.
"""

import pytest
from app.ai.embeddings.encoder import generate_embedding, generate_batch_embeddings
from app.ai.embeddings.faiss_store import FAISSVectorStore


def test_generate_embedding():
    text = "Senior Python Developer with experience in FastAPI and Docker."
    vec = generate_embedding(text)
    assert len(vec) == 384
    assert isinstance(vec[0], float)


def test_generate_batch_embeddings():
    texts = ["Python Developer", "React Frontend Engineer"]
    vecs = generate_batch_embeddings(texts)
    assert len(vecs) == 2
    assert len(vecs[0]) == 384


def test_faiss_store(tmp_path):
    index_path = str(tmp_path / "test_faiss")
    store = FAISSVectorStore(dimension=384, index_path=index_path)

    v1 = generate_embedding("Python FastAPI Developer")
    v2 = generate_embedding("Java Spring Boot Developer")

    id1 = "uuid-1111"
    id2 = "uuid-2222"

    store.add_vector(id1, v1)
    store.add_vector(id2, v2)

    query_v = generate_embedding("Python Engineer")
    results = store.search(query_v, top_k=2)

    assert len(results) == 2
    top_entity_id, score = results[0]
    # Python vector should match Python Engineer better than Java vector
    assert top_entity_id == id1
    assert score > 0.5
