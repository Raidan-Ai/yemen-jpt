"""Contract tests — validate schema correctness."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'packages', 'contracts', 'src'))

import uuid
from datetime import datetime, timezone
from yemenjpt_contracts.schemas.events import CanonicalEvent, SourceRef, Producer, Confidence, ConfidenceLabel, FactTaxonomy, VerificationStatus

def test_canonical_event_valid():
    e = CanonicalEvent(
        event_type="test.event",
        source=SourceRef(source_id="src1"),
        producer=Producer(agent_id="test_agent"),
    )
    assert e.event_type == "test.event"
    assert e.confidence.label == ConfidenceLabel.UNKNOWN
    assert isinstance(e.event_id, str)
    assert len(e.event_id) == 36

def test_canonical_event_empty_type_fails():
    import pytest
    with pytest.raises(Exception):
        CanonicalEvent(
            event_type="   ",
            source=SourceRef(source_id="src1"),
            producer=Producer(agent_id="agent"),
        )

def test_confidence_bounds():
    import pytest
    with pytest.raises(Exception):
        Confidence(score=1.5)
    with pytest.raises(Exception):
        Confidence(score=-0.1)

def test_fact_taxonomy_values():
    assert FactTaxonomy.FACT == "FACT"
    assert FactTaxonomy.CLAIM == "CLAIM"
    assert FactTaxonomy.INFERENCE == "INFERENCE"
    assert FactTaxonomy.PREDICTION == "PREDICTION"

def test_verification_status():
    assert VerificationStatus.UNKNOWN == "unknown"
    assert VerificationStatus.MIXED == "mixed"

def test_event_bus_singleton():
    from yemenjpt_contracts.services.event_bus import get_event_bus
    b1 = get_event_bus()
    b2 = get_event_bus()
    assert b1 is b2

def test_event_bus_subscribe_publish(event_loop):
    import asyncio
    from yemenjpt_contracts.services.event_bus import InProcessEventBus
    from yemenjpt_contracts.schemas.events import CanonicalEvent, SourceRef, Producer

    bus = InProcessEventBus()
    received = []

    async def handler(ev: CanonicalEvent):
        received.append(ev.event_type)

    bus.subscribe("test.publish", handler)

    event = CanonicalEvent(
        event_type="test.publish",
        source=SourceRef(source_id="test"),
        producer=Producer(agent_id="test"),
    )

    async def run():
        await bus.start()
        await bus.publish(event)
        await asyncio.sleep(0.2)
        await bus.stop()

    asyncio.get_event_loop().run_until_complete(run())
    assert "test.publish" in received
