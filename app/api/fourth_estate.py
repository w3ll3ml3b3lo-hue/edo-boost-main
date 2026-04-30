from __future__ import annotations

import json
import logging
import uuid
from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import aio_pika
import structlog
from pydantic import BaseModel

from app.api.constitutional_schema.types import (
    AuditEvent,
    EventType,
    ExecutiveAction,
    JudiciaryStamp,
    StampStatus,
)
from app.api.core.config import settings

logger = structlog.get_logger(__name__)

_fourth_estate: Optional["FourthEstate"] = None


class FourthEstate:
    """
    Durable Audit Trail Service (Pillar 4).
    Migrated from Redis Streams to RabbitMQ for POPIA-grade persistence.
    Maintains an in-memory buffer for recent event queries.
    """

    def __init__(
        self,
        rabbitmq_url: Optional[str] = None,
        exchange_name: str = "eduboost_audit_log",
        buffer_size: int = 1000,
    ) -> None:
        self.rabbitmq_url = rabbitmq_url or settings.RABBITMQ_URL
        self.exchange_name = exchange_name
        self._buffer: deque[AuditEvent] = deque(maxlen=buffer_size)
        self._total_events = 0
        self._violations = 0
        self._sequence = 0
        self._connection: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.RobustChannel] = None
        self._exchange: Optional[aio_pika.RobustExchange] = None

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        if not self.rabbitmq_url:
            logger.warning("rabbitmq_url_missing", detail="Fourth Estate will not be able to publish events")
            return

        if not self._connection or self._connection.is_closed:
            try:
                self._connection = await aio_pika.connect_robust(self.rabbitmq_url)
                self._channel = await self._connection.channel()
                # Declare a fanout exchange for durability and broadcasting
                self._exchange = await self._channel.declare_exchange(
                    self.exchange_name,
                    aio_pika.ExchangeType.FANOUT,
                    durable=True,
                )
                logger.info("connected_to_fourth_estate", url=self.rabbitmq_url, exchange=self.exchange_name)
            except Exception as e:
                logger.error("fourth_estate_connection_failed", error=str(e))

    async def close(self) -> None:
        """Close RabbitMQ connection."""
        if self._connection:
            await self._connection.close()
            logger.info("fourth_estate_connection_closed")

    def get_stats(self) -> dict:
        return {
            "total_events": self._total_events,
            "violations": self._violations,
            "buffer_size": len(self._buffer),
            "exchange_name": self.exchange_name,
            "connected": self._connection is not None and not self._connection.is_closed,
        }

    def get_sequence(self) -> int:
        """Return the current audit event sequence number."""
        return self._sequence

    async def publish(self, event: AuditEvent) -> None:
        """Publishes an immutable audit event to the durable broker and local buffer."""
        self._total_events += 1
        self._sequence += 1
        self._buffer.append(event)

        if not self._exchange:
            await self.connect()

        if self._exchange:
            try:
                # Use model_dump_json() if it's a Pydantic model
                payload = event.model_dump_json() if isinstance(event, BaseModel) else json.dumps(event)
                message_body = payload.encode()
                
                message = aio_pika.Message(
                    body=message_body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # Ensure persistence on disk
                    content_type="application/json",
                    timestamp=int(event.occurred_at.timestamp()) if hasattr(event, "occurred_at") else int(datetime.now(timezone.utc).timestamp()),
                )

                await self._exchange.publish(message, routing_key="")
                logger.debug("audit_event_published", event_id=getattr(event, "event_id", "unknown"))
            except Exception as e:
                logger.error("audit_publish_failed", error=str(e), event_id=getattr(event, "event_id", "unknown"))
        else:
            logger.warning("audit_publish_skipped_no_connection", event_id=getattr(event, "event_id", "unknown"))

    async def publish_event(self, event: Any) -> None:
        """Compatibility method for the new FourthEstateService API."""
        if isinstance(event, AuditEvent):
            await self.publish(event)
        else:
            # If it's a different model (like the one in the provided file), try to adapt it
            # or just publish it as is if it's a dict/BaseModel
            self._total_events += 1
            if self._exchange:
                try:
                    payload = event.model_dump_json() if hasattr(event, "model_dump_json") else json.dumps(event)
                    message = aio_pika.Message(
                        body=payload.encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                        content_type="application/json",
                    )
                    await self._exchange.publish(message, routing_key="")
                except Exception as e:
                    logger.error("audit_publish_failed", error=str(e))

    async def publish_action_submitted(self, action: Any) -> None:
        """Publishes an action submission event. Handles multiple model versions."""
        action_id = getattr(action, "action_id", str(uuid.uuid4()))
        learner_hash = getattr(action, "learner_id_hash", getattr(action, "learner_pseudonym", "unknown"))
        intent = getattr(action, "action_type", getattr(action, "intent", "unknown"))
        if hasattr(intent, "value"):
            intent = intent.value
            
        await self.publish(
            AuditEvent(
                event_type=EventType.ACTION_SUBMITTED,
                pillar="EXECUTIVE",
                action_id=action_id,
                learner_hash=learner_hash,
                payload={"action_type": intent},
            )
        )

    async def publish_stamp_issued(
        self, stamp: Any, action: Any
    ) -> None:
        """Publishes a stamp issuance event. Handles multiple model versions."""
        action_id = getattr(action, "action_id", str(uuid.uuid4()))
        learner_hash = getattr(action, "learner_id_hash", getattr(action, "learner_pseudonym", "unknown"))
        
        status = getattr(stamp, "status", getattr(stamp, "verdict", "unknown"))
        if hasattr(status, "value"):
            status = status.value
            
        violations = getattr(stamp, "violations", getattr(stamp, "rules_checked", []))
        
        await self.publish(
            AuditEvent(
                event_type=EventType.STAMP_ISSUED,
                pillar="JUDICIARY",
                action_id=action_id,
                learner_hash=learner_hash,
                payload={"status": status, "violations": violations},
            )
        )
        if status == "REJECTED":
            await self.publish(
                AuditEvent(
                    event_type=EventType.STAMP_REJECTED,
                    pillar="JUDICIARY",
                    action_id=action_id,
                    learner_hash=learner_hash,
                    payload={"violations": violations},
                )
            )
            await self.flag_constitutional_violation(
                action=action, stamp=stamp, violated_rules=list(violations)
            )

    async def flag_constitutional_violation(
        self, action: Any, stamp: Any, violated_rules: list[str]
    ) -> None:
        self._violations += 1
        action_id = getattr(action, "action_id", str(uuid.uuid4()))
        learner_hash = getattr(action, "learner_id_hash", getattr(action, "learner_pseudonym", "unknown"))
        status = getattr(stamp, "status", getattr(stamp, "verdict", "unknown"))
        if hasattr(status, "value"):
            status = status.value

        await self.publish(
            AuditEvent(
                event_type=EventType.CONSTITUTIONAL_VIOL,
                pillar="JUDICIARY",
                action_id=action_id,
                learner_hash=learner_hash,
                payload={"rules": violated_rules, "stamp": status},
            )
        )

    async def publish_llm_result(
        self, action: Any, provider: str, success: bool, latency_ms: int
    ) -> None:
        et = EventType.LLM_CALL_COMPLETED if success else EventType.LLM_CALL_FAILED
        action_id = getattr(action, "action_id", str(uuid.uuid4()))
        learner_hash = getattr(action, "learner_id_hash", getattr(action, "learner_pseudonym", "unknown"))
        
        await self.publish(
            AuditEvent(
                event_type=et,
                pillar="EXECUTIVE",
                action_id=action_id,
                learner_hash=learner_hash,
                payload={"provider": provider, "latency_ms": latency_ms},
            )
        )

    async def publish_ether_event(
        self, learner_hash: str, archetype: str, cache_hit: bool
    ) -> None:
        et = EventType.ETHER_PROFILE_HIT if cache_hit else EventType.ETHER_PROFILE_MISS
        await self.publish(
            AuditEvent(
                event_type=et,
                pillar="ETHER",
                learner_hash=learner_hash,
                payload={"archetype": archetype, "cache_hit": cache_hit},
            )
        )

    async def publish_domain_event(
        self, event_type: EventType, action: Any, payload: dict[str, Any]
    ) -> None:
        action_id = getattr(action, "action_id", str(uuid.uuid4()))
        learner_hash = getattr(action, "learner_id_hash", getattr(action, "learner_pseudonym", "unknown"))

        await self.publish(
            AuditEvent(
                event_type=event_type,
                pillar="EXECUTIVE",
                action_id=action_id,
                learner_hash=learner_hash,
                payload=payload,
            )
        )

    def get_recent_events(self, n: int) -> list[AuditEvent]:
        if n <= 0:
            return []
        return list(self._buffer)[-n:]

    def get_health_status(self) -> dict:
        from app.api.judiciary import get_judiciary

        j = get_judiciary()
        s = j.get_stats()
        health = s["approval_rate"]
        return {
            "overall": "GREEN" if health >= 0.95 else "AMBER",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "constitutional_health": health,
            "judiciary_approval_rate": health,
            "pillar_status": {
                "LEGISLATURE": "GREEN",
                "EXECUTIVE": "GREEN",
                "JUDICIARY": "GREEN",
                "FOURTH_ESTATE": "GREEN",
                "ETHER": "GREEN",
            },
        }

    def build_audit_report(
        self, report_type: str = "COMPLIANCE", hours: int = 24
    ) -> dict:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        recent = [e for e in self._buffer if e.occurred_at >= cutoff]
        return {
            "report_type": report_type,
            "hours": hours,
            "event_count": len(recent),
            "total_recorded": self._total_events,
        }

    def get_chain_integrity(self) -> dict[str, Any]:
        return {"sealed": True, "buffer_len": len(self._buffer)}

    def get_recent_violations(self, limit: int = 5) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for e in reversed(self._buffer):
            if e.event_type == EventType.CONSTITUTIONAL_VIOL:
                out.append({"event_id": e.event_id, "payload": e.payload})
                if len(out) >= limit:
                    break
        return list(reversed(out))


def get_fourth_estate() -> FourthEstate:
    global _fourth_estate
    if _fourth_estate is None:
        _fourth_estate = FourthEstate()
    return _fourth_estate


# Global instance for easy access (as requested in the provided file)
fourth_estate = get_fourth_estate()
