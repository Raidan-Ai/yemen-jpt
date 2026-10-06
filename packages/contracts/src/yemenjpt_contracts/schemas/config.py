from pydantic import BaseModel, Field
from typing import Any


class ConfigEnvelope(BaseModel):
    """"Configuration envelope for YemenJPT.""""
    environment: str = "development"
    model_provider: str = "litellm"
    features: dict[str, Any] = Field(default_factory=dict)
    thresholds: dict[str, Any] = Field(default_factory=dict)
