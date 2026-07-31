"""
Integration tests for authentication API endpoints.
Uses in-memory SQLite and the AsyncClient fixture from conftest.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestRegister:
    async def test_register_candidate_success(self, client: AsyncClient, candidate_payload):
        response = await client.post("/auth/register", json=candidate_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "verification email" in data["message"].lower()

    async def test_register_recruiter_success(self, client: AsyncClient, recruiter_payload):
        response = await client.post("/auth/register", json=recruiter_payload)
        assert response.status_code == 201

    async def test_register_duplicate_email(self, client: AsyncClient, candidate_payload):
        await client.post("/auth/register", json=candidate_payload)
        response = await client.post("/auth/register", json=candidate_payload)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()

    async def test_register_weak_password(self, client: AsyncClient):
        payload = {
            "name": "Test User",
            "email": "test@test.com",
            "password": "weak",
            "role": "candidate",
        }
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 422  # validation error

    async def test_register_invalid_email(self, client: AsyncClient):
        payload = {
            "name": "Test User",
            "email": "not-an-email",
            "password": "TestPass123!",
            "role": "candidate",
        }
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 422

    async def test_register_missing_fields(self, client: AsyncClient):
        response = await client.post("/auth/register", json={})
        assert response.status_code == 422


@pytest.mark.integration
class TestLogin:
    async def test_login_success(self, client: AsyncClient, candidate_payload, db):
        """Register a user, verify email manually, then login."""
        await client.post("/auth/register", json=candidate_payload)

        # Manually verify email in test DB
        from app.repositories.user_repository import UserRepository
        repo = UserRepository(db)
        user = await repo.get_by_email(candidate_payload["email"])
        assert user is not None
        await repo.verify_email(user.id)
        await db.commit()

        response = await client.post(
            "/auth/login",
            json={
                "email": candidate_payload["email"],
                "password": candidate_payload["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == candidate_payload["email"]

    async def test_login_wrong_password(self, client: AsyncClient, candidate_payload):
        await client.post("/auth/register", json=candidate_payload)
        response = await client.post(
            "/auth/login",
            json={"email": candidate_payload["email"], "password": "WrongPass123!"},
        )
        assert response.status_code == 401

    async def test_login_nonexistent_email(self, client: AsyncClient):
        response = await client.post(
            "/auth/login",
            json={"email": "ghost@test.com", "password": "TestPass123!"},
        )
        assert response.status_code == 401


@pytest.mark.integration
class TestProtectedEndpoints:
    async def _get_token(self, client: AsyncClient, payload: dict, db) -> str:
        """Helper: register, verify, login, return access token."""
        await client.post("/auth/register", json=payload)
        from app.repositories.user_repository import UserRepository
        repo = UserRepository(db)
        user = await repo.get_by_email(payload["email"])
        await repo.verify_email(user.id)
        await db.commit()
        resp = await client.post(
            "/auth/login",
            json={"email": payload["email"], "password": payload["password"]},
        )
        return resp.json()["access_token"]

    async def test_get_me_authenticated(self, client: AsyncClient, candidate_payload, db):
        token = await self._get_token(client, candidate_payload, db)
        response = await client.get(
            "/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == candidate_payload["email"]

    async def test_get_me_unauthenticated(self, client: AsyncClient):
        response = await client.get("/auth/me")
        assert response.status_code == 401

    async def test_get_me_invalid_token(self, client: AsyncClient):
        response = await client.get(
            "/auth/me", headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401


@pytest.mark.integration
class TestForgotResetPassword:
    async def test_forgot_password_always_200(self, client: AsyncClient):
        """Security: always returns 200 regardless of email existence."""
        response = await client.post(
            "/auth/forgot-password",
            json={"email": "nonexistent@test.com"},
        )
        assert response.status_code == 200

    async def test_reset_invalid_token(self, client: AsyncClient):
        response = await client.post(
            "/auth/reset-password",
            json={"token": "invalid-token", "new_password": "NewPass123!"},
        )
        assert response.status_code == 400
