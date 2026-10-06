"""Application-level event bus service wrapper."""
from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'packages', 'contracts', 'src'))

from yemenjpt_contracts.services.event_bus import InProcessEventBus, get_event_bus

_bus: InProcessEventBus | None = None


def get_bus() -> InProcessEventBus:
    return get_event_bus()
