"""Provider factory — instantiate correct router based on settings."""
from __future__ import annotations
from functools import lru_cache

from .router import ModelRouter
from ..config.settings import get_settings


@lru_cache(maxsize=1)
def get_model_router() -> ModelRouter:
    s = get_settings()
    if s.MODEL_PROVIDER.lower() == "openai" and s.OPENAI_API_KEY:
        from .openai_provider import OpenAIModelRouter
        return OpenAIModelRouter()
    from .mock_provider import MockModelRouter
    return MockModelRouter()
