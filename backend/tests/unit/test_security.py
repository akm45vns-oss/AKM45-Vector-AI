"""
Unit tests for the security module — no DB required.
"""

import pytest
from jose import JWTError

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_secure_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_is_not_plain_text(self):
        hashed = hash_password("MySecret123!")
        assert hashed != "MySecret123!"

    def test_verify_correct_password(self):
        hashed = hash_password("MySecret123!")
        assert verify_password("MySecret123!", hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("MySecret123!")
        assert verify_password("WrongPass!", hashed) is False

    def test_two_hashes_are_different(self):
        """bcrypt uses random salt — same input produces different hashes."""
        h1 = hash_password("SamePass123!")
        h2 = hash_password("SamePass123!")
        assert h1 != h2


class TestJWT:
    def test_access_token_decodes_correctly(self):
        token = create_access_token("user-uuid-123", "candidate")
        payload = decode_token(token)
        assert payload.sub == "user-uuid-123"
        assert payload.role == "candidate"
        assert payload.type == "access"

    def test_refresh_token_type(self):
        token = create_refresh_token("user-uuid-123", "recruiter")
        payload = decode_token(token)
        assert payload.type == "refresh"

    def test_invalid_token_raises(self):
        with pytest.raises(JWTError):
            decode_token("this.is.not.valid")

    def test_tampered_token_raises(self):
        token = create_access_token("user-uuid-123", "candidate")
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(JWTError):
            decode_token(tampered)


class TestSecureToken:
    def test_token_length(self):
        token = generate_secure_token(32)
        assert len(token) > 0

    def test_tokens_are_unique(self):
        tokens = {generate_secure_token(32) for _ in range(100)}
        assert len(tokens) == 100  # all unique
