"""OpenAI provider — used when MODEL_PROVIDER=openai."""
from __future__ import annotations
import json
from typing import Any

import httpx

from .router import Capability, ModelRouter
from ..config.settings import get_settings


class OpenAIModelRouter(ModelRouter):
    def __init__(self) -> None:
        s = get_settings()
        self._base = s.OPENAI_BASE_URL
        self._key = s.OPENAI_API_KEY
        self._models: dict[Capability, str] = {
            Capability.REASONING: s.MODEL_REASONING,
            Capability.EXTRACTION: s.MODEL_EXTRACTION,
            Capability.CLASSIFICATION: s.MODEL_CLASSIFICATION,
            Capability.TRANSLATION: s.MODEL_TRANSLATION,
            Capability.VISION: s.MODEL_VISION,
            Capability.SUMMARIZATION: s.MODEL_EXTRACTION,
            Capability.CODING: s.MODEL_REASONING,
            Capability.EMBEDDING: s.MODEL_EMBEDDING,
        }

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
        }

    async def generate_text(
        self,
        capability: Capability,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"{self._base}/chat/completions",
                headers=self._headers(),
                json={
                    "model": self._models[capability],
                    "messages": messages,
                    **kwargs,
                },
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]

    async def extract_structured(
        self,
        prompt: str,
        schema_description: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        messages = [
            {
                "role": "system",
                "content": (
                    f"Schema: {schema_description}\n"
                    "Respond with valid JSON only. No markdown fences."
                ),
            },
            {"role": "user", "content": prompt},
        ]
        text = await self.generate_text(
            Capability.EXTRACTION,
            messages,
            response_format={"type": "json_object"},
        )
        return json.loads(text)

    async def embed(self, text: str, **kwargs: Any) -> list[float]:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                f"{self._base}/embeddings",
                headers=self._headers(),
                json={
                    "model": self._models[Capability.EMBEDDING],
                    "input": text,
                },
            )
            r.raise_for_status()
            return r.json()["data"][0]["embedding"]

    async def classify(
        self,
        text: str,
        labels: list[str],
        **kwargs: Any,
    ) -> dict[str, float]:
        prompt = (
            f"Classify the following text into exactly one of these categories: {labels}\n\n"
            f"Text: {text}\n\n"
            'Respond with JSON: {"label": "<chosen_label>", "confidence": <0.0-1.0>}'
        )
        messages = [{"role": "user", "content": prompt}]
        raw = await self.generate_text(
            Capability.CLASSIFICATION,
            messages,
            response_format={"type": "json_object"},
        )
        data = json.loads(raw)
        chosen = data.get("label", labels[0])
        conf = float(data.get("confidence", 0.5))
        remainder = (1.0 - conf) / max(len(labels) - 1, 1)
        return {
            label: (conf if label == chosen else remainder)
            for label in labels
        }
