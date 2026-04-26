"""Integration tests for authentication lifecycle."""
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.main import app


@pytest.mark.asyncio
@pytest.mark.integration
async def test_guardian_login_invalid_credentials():
    """Test that login fails gracefully with invalid guardian credentials."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/guardian/login",
            json={
                "email": "invalid@example.com",
                "learner_pseudonym_id": str(uuid.uuid4()),
            },
        )

    # We expect 401 or 404 since the learner doesn't exist
    assert response.status_code in [401, 404]
    if response.status_code == 401:
        payload = response.json()
        assert "INVALID_GUARDIAN_CREDENTIALS" in payload["detail"]["code"]


@pytest.mark.asyncio
@pytest.mark.integration
async def test_learner_session_creation():
    """Test that learner session endpoint returns a valid JWT token."""
    learner_id = str(uuid.uuid4())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/learner/session",
            json={
                "learner_id": learner_id,
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert "session_token" in payload
    assert "expires_in" in payload
    
    # Verify it looks like a JWT
    assert len(payload["session_token"].split(".")) == 3
