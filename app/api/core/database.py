"""
EduBoost SA — Async Database Engine & Session Factory
"""
from __future__ import annotations

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.api.core.config import settings

_is_sqlite = settings.DATABASE_URL.strip().lower().startswith("sqlite")

if _is_sqlite:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
    )
else:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
    )

AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
_schema_initialized = False
_schema_lock = asyncio.Lock()


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    global _schema_initialized
    if _is_sqlite and not _schema_initialized:
        async with _schema_lock:
            if not _schema_initialized:
                await init_test_schema()
                _schema_initialized = True

    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_test_schema() -> None:
    """
    For local test runs (eg. pytest without Docker/Postgres), create the schema
    for SQLite-backed test DBs. Production and normal dev rely on Alembic.
    """
    if not _is_sqlite:
        return

    # Import all models so metadata is fully populated.
    from app.api.models import db_models as _db_models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
