"""
EduBoost SA — Dummy Data Generator (post-startup)

Generates up to N dummy data points in the background after startup.
Supports a persistence floor by marking a subset as persistent and only
cleaning up non-persistent points when exceeding the target.
"""

from __future__ import annotations

import asyncio
import random
import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import delete, func, select

from app.api.core.config import settings
from app.api.core.database import AsyncSessionFactory
from app.api.models.db_models import DummyDataPoint

log = structlog.get_logger()

_GEN_LOCK = asyncio.Lock()


def _clamp_ratio(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


class DummyDataService:
    async def run_startup_generation(self) -> None:
        """
        Fire-and-forget entrypoint: wait for startup, then generate quietly.
        """
        if not settings.DUMMY_DATA_ENABLED:
            return
        if settings.APP_ENV == "test":
            return

        try:
            await asyncio.sleep(max(0, int(settings.DUMMY_DATA_START_DELAY_SECONDS)))
            await self.ensure_target_points()
        except Exception as e:
            # Silent by default: only surface errors.
            log.error("dummy_data.startup.failed", error=str(e))

    async def ensure_target_points(self) -> None:
        target = int(settings.DUMMY_DATA_TARGET)
        if target <= 0:
            return

        min_ratio = float(settings.DUMMY_DATA_PERSIST_MIN_RATIO)
        max_ratio = float(settings.DUMMY_DATA_PERSIST_MAX_RATIO)
        min_ratio = _clamp_ratio(min_ratio, 0.0, 1.0)
        max_ratio = _clamp_ratio(max_ratio, min_ratio, 1.0)

        persistent_floor = int(target * min_ratio)
        kind = settings.DUMMY_DATA_KIND or "synthetic"
        batch_size = max(1, int(settings.DUMMY_DATA_BATCH_SIZE))

        async with _GEN_LOCK:
            async with AsyncSessionFactory() as session:
                existing = await session.scalar(select(func.count()).select_from(DummyDataPoint).where(DummyDataPoint.kind == kind))
                existing = int(existing or 0)

                persistent_existing = await session.scalar(
                    select(func.count()).select_from(DummyDataPoint).where(
                        DummyDataPoint.kind == kind,
                        DummyDataPoint.is_persistent == True,  # noqa: E712
                    )
                )
                persistent_existing = int(persistent_existing or 0)

                to_create = max(0, target - existing)
                if to_create <= 0:
                    await self._cleanup_if_needed(session=session, kind=kind, target=target, persistent_floor=persistent_floor)
                    return

                # Create in batches.
                while to_create > 0:
                    n = min(batch_size, to_create)
                    now = datetime.now(timezone.utc).isoformat()
                    items: list[DummyDataPoint] = []
                    for _ in range(n):
                        # Ensure at least the persistent floor is satisfied.
                        mark_persistent = persistent_existing < persistent_floor
                        if mark_persistent:
                            persistent_existing += 1

                        items.append(
                            DummyDataPoint(
                                data_id=uuid.uuid4(),
                                kind=kind,
                                is_persistent=mark_persistent,
                                payload={
                                    "ts": now,
                                    "value": random.random(),
                                    "label": random.choice(["alpha", "beta", "gamma", "delta"]),
                                    "source": "dummy-generator",
                                },
                            )
                        )

                    session.add_all(items)
                    await session.commit()
                    to_create -= n

                await self._cleanup_if_needed(session=session, kind=kind, target=target, persistent_floor=persistent_floor)

    async def _cleanup_if_needed(self, session, kind: str, target: int, persistent_floor: int) -> None:
        total = await session.scalar(select(func.count()).select_from(DummyDataPoint).where(DummyDataPoint.kind == kind))
        total = int(total or 0)
        if total <= target:
            return

        persistent_count = await session.scalar(
            select(func.count()).select_from(DummyDataPoint).where(
                DummyDataPoint.kind == kind,
                DummyDataPoint.is_persistent == True,  # noqa: E712
            )
        )
        persistent_count = int(persistent_count or 0)
        # Never delete persistent points; if they exceed target we just keep them.
        if persistent_count >= target:
            return

        # Delete oldest non-persistent points until within target.
        to_delete = max(0, total - target)
        if to_delete <= 0:
            return

        ids = await session.execute(
            select(DummyDataPoint.data_id)
            .where(DummyDataPoint.kind == kind, DummyDataPoint.is_persistent == False)  # noqa: E712
            .order_by(DummyDataPoint.created_at.asc())
            .limit(to_delete)
        )
        id_list = [row[0] for row in ids.all()]
        if not id_list:
            return

        await session.execute(delete(DummyDataPoint).where(DummyDataPoint.data_id.in_(id_list)))
        await session.commit()


dummy_data_service = DummyDataService()

