"""AI Model Router — capability-based abstraction."""
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class Capability(str, Enum):
    REASONING = "reasoning"
    EXTRACTION = "extraction"
    CLASSIFICATION = "classification"
    TRANSLATION = "translation"
    EMBEDDING = "embedding"
    VISION = "vision"
    CODING = "coding"
    SUMMARIZATION = "summarization"


class ModelRouter(ABC):
    @abstractmethod
    async def generate_text(
        self,
        capability: Capability,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str: ...

    @abstractmethod
    async def extract_structured(
        self,
        prompt: str,
        schema_description: str,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    @abstractmethod
    async def embed(self, text: str, **kwargs: Any) -> list[float]: ...

    @abstractmethod
    async def classify(
        self,
        text: str,
        labels: list[str],
        **kwargs: Any,
    ) -> dict[str, float]: ...
