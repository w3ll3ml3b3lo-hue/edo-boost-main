import pytest
import pytest_asyncio
import uuid
from sqlalchemy import text
from app.api.core.database import AsyncSessionFactory, init_test_schema

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Initialize the test database schema once per session."""
    await init_test_schema()

@pytest_asyncio.fixture(autouse=True)
async def seed_consent():
    """Ensure active consent for common test learner IDs."""
    async with AsyncSessionFactory() as session:
        # Standard test IDs from integration tests
        test_ids = [
            "00000000-0000-0000-0000-000000000001",
            "00000000-0000-0000-0000-000000000002",
            "6013627d-9477-493a-86c4-1188383e5898", # Example valid UUID
        ]
        
        # We also need to handle string 'pseudonyms' if tests use them, 
        # but the DB model has UUID. If it's SQLite, it might just work.
        
        for lid in test_ids:
            try:
                await session.execute(
                    text("""
                        INSERT INTO consent_audit (audit_id, pseudonym_id, event_type, occurred_at)
                        VALUES (:aid, :lid, 'consent_granted', CURRENT_TIMESTAMP)
                    """),
                    {"aid": str(uuid.uuid4()), "lid": lid}
                )
            except Exception:
                # Likely already exists or integrity error, skip for seed
                await session.rollback()
                continue
        await session.commit()
