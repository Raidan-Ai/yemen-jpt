"""Base agent — 02_AGENT_CONTRACTS.md."""
from __future__ import annotations
import logging, sys, os
from abc import ABC, abstractmethod
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))
from yemenjpt_contracts.schemas.events import CanonicalEvent, Producer, SourceRef
from yemenjpt_contracts.services.event_bus import InProcessEventBus

class BaseAgent(ABC):
    agent_id: str = "base"
    version: str = "1.0"
    purpose: str = ""
    input_event_types: list[str] = []
    output_event_types: list[str] = []
    prohibited_actions: list[str] = ["fabricate_evidence", "mutate_other_agent_state"]

    def __init__(self):
        self.logger = logging.getLogger(f"yemenjpt.agents.{self.agent_id}")

    def register(self, bus: InProcessEventBus) -> None:
        for et in self.input_event_types:
            bus.subscribe(et, self.handle)
        self.logger.info("Agent %s registered for %s", self.agent_id, self.input_event_types)

    async def handle(self, event: CanonicalEvent) -> None:
        try:
            await self.process(event)
        except Exception as exc:
            self.logger.exception("Agent %s failed: %s", self.agent_id, exc)
            raise

    @abstractmethod
    async def process(self, event: CanonicalEvent) -> None: ...

    def make_producer(self) -> Producer:
        return Producer(agent_id=self.agent_id, agent_version=self.version)
