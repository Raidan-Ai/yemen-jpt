"""
In-process asyncio Event Bus with dead-letter and retry.
ADR-0002: interface supports future Redis Streams / NATS swap.
"""
from __future__ import annotations
import asyncio
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Callable, Awaitable

from ..schemas.events import CanonicalEvent

logger = logging.getLogger(__name__)
EventHandler = Callable[[CanonicalEvent], Awaitable[None]]


class DeadLetterEntry:
    def __init__(self, event: CanonicalEvent, reason: str, attempts: int) -> None:
        self.event = event
        self.reason = reason
        self.attempts = attempts
        self.timestamp = datetime.now(timezone.utc)


class InProcessEventBus:
    def __init__(self, max_retries: int = 3) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._wildcards: list[EventHandler] = []
        self._dead_letter: list[DeadLetterEntry] = []
        self._processed: dict[str, datetime] = {}
        self._max_retries = max_retries
        self._queue: asyncio.Queue[CanonicalEvent] = asyncio.Queue()
        self._running = False
        self._worker: asyncio.Task | None = None

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type == "*":
            self._wildcards.append(handler)
        else:
            self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type == "*":
            self._wildcards.remove(handler)
        else:
            self._handlers[event_type].remove(handler)

    async def publish(self, event: CanonicalEvent) -> None:
        if event.event_id in self._processed:
            return
        await self._queue.put(event)

    async def acknowledge(self, event_id: str) -> None:
        self._processed[event_id] = datetime.now(timezone.utc)

    async def dead_letter(self, event: CanonicalEvent, reason: str, attempts: int) -> None:
        self._dead_letter.append(DeadLetterEntry(event, reason, attempts))
        logger.warning("Dead-lettered %s: %s", event.event_id, reason)

    def get_dead_letters(self) -> list[DeadLetterEntry]:
        return list(self._dead_letter)

    async def start(self) -> None:
        self._running = True
        self._worker = asyncio.create_task(self._run())

    async def stop(self) -> None:
        self._running = False
        if self._worker:
            self._worker.cancel()
            try:
                await self._worker
            except asyncio.CancelledError:
                pass

    async def _run(self) -> None:
        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await self._dispatch(event)
                self._queue.task_done()
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    async def _dispatch(self, event: CanonicalEvent, attempt: int = 1) -> None:
        handlers = list(self._handlers.get(event.event_type, [])) + list(self._wildcards)
        if not handlers:
            await self.acknowledge(event.event_id)
            return
        errors: list[Exception] = []
        for h in handlers:
            try:
                await h(event)
            except Exception as exc:
                errors.append(exc)
        if errors and attempt < self._max_retries:
            await self._dispatch(event, attempt + 1)
        elif errors:
            await self.dead_letter(event, str(errors[0]), attempt)
        else:
            await self.acknowledge(event.event_id)


_bus: InProcessEventBus | None = None


def get_event_bus() -> InProcessEventBus:
    global _bus
    if _bus is None:
        _bus = InProcessEventBus()
    return _bus
