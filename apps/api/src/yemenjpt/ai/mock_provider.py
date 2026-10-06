"""Deterministic mock AI provider — zero external dependencies."""
from __future__ import annotations
import hashlib
import math
from typing import Any

from .router import Capability, ModelRouter


class MockModelRouter(ModelRouter):
    async def generate_text(
        self,
        capability: Capability,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        content = " ".join(m.get("content", "") for m in messages)
        h = int(hashlib.md5(content.encode()).hexdigest(), 16) % 1000
        return (
            f"[SYNTHETIC] Mock {capability.value} response (hash={h}). "
            "This is development fixture data — not real intelligence."
        )

    async def extract_structured(
        self,
        prompt: str,
        schema_description: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        h = int(hashlib.md5(prompt.encode()).hexdigest(), 16) % 100
        return {
            "_synthetic": True,
            "_dev_note": "SYNTHETIC/DEVELOPMENT DATA",
            "entities": [
                {
                    "name": f"Entity-{h}",
                    "type": "Organization",
                    "confidence": 0.3,
                    "note": "synthetic",
                }
            ],
            "claims": [
                {
                    "text": f"Synthetic claim {h}.",
                    "taxonomy": "CLAIM",
                    "confidence": 0.2,
                    "note": "synthetic",
                }
            ],
            "relationships": [],
        }

    async def embed(self, text: str, **kwargs: Any) -> list[float]:
        raw = [(b - 128) / 128.0 for b in hashlib.sha256(text.encode()).digest()]
        vec = [raw[i % len(raw)] for i in range(384)]
        mag = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / mag for x in vec]

    async def classify(
        self,
        text: str,
        labels: list[str],
        **kwargs: Any,
    ) -> dict[str, float]:
        if not labels:
            return {}
        u = 1.0 / len(labels)
        return {label: u for label in labels}
