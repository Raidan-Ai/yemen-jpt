"""Workflow test — end-to-end: source -> agents -> case -> report."""
import asyncio
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'packages', 'contracts', 'src'))

from yemenjpt_contracts.schemas.events import CanonicalEvent, SourceRef, Producer
from yemenjpt_contracts.services.event_bus import InProcessEventBus

def test_ingestion_agent_emits_ingested_event():
    """Ingestion agent processes source.submit and emits source.ingested."""
    import asyncio
    from yemenjpt.agents.ingestion import IngestionAgent

    received = []
    bus = InProcessEventBus()

    async def capture(ev: CanonicalEvent):
        received.append(ev.event_type)

    bus.subscribe("source.ingested", capture)
    agent = IngestionAgent()
    agent.register(bus)

    async def run():
        await bus.start()
        ev = CanonicalEvent(
            event_type="source.submit",
            source=SourceRef(source_id="test_source"),
            producer=Producer(agent_id="test"),
            payload={"content": "SYNTHETIC TEST: Yemen currency crisis report.", "url": "http://example.com/article", "source_id": "src_test_001", "language": "en"},
        )
        await bus.publish(ev)
        await asyncio.sleep(0.5)
        await bus.stop()

    asyncio.get_event_loop().run_until_complete(run())
    assert "source.ingested" in received

def test_research_api_creates_mission(client):
    """Research endpoint returns mission_id."""
    r = client.post("/api/v1/research", json={
        "question": "SYNTHETIC TEST: What are the economic impacts of the Yemen conflict?",
    })
    assert r.status_code == 200
    assert "mission_id" in r.json()
    assert r.json()["status"] == "pending"

def test_full_case_workflow(client):
    """Create case -> submit research -> check case has events (eventually)."""
    # 1. Create case
    case_r = client.post("/api/v1/cases", json={
        "title": "SYNTHETIC TEST CASE",
        "research_question": "What happened in Aden in 2015?",
    })
    assert case_r.status_code == 201
    case_id = case_r.json()["case_id"]

    # 2. Submit research
    res_r = client.post("/api/v1/research", json={
        "question": "SYNTHETIC TEST: Investigate Aden 2015 events.",
        "case_id": case_id,
    })
    assert res_r.status_code == 200
    assert "mission_id" in res_r.json()

    # 3. Case still accessible
    case_get = client.get(f"/api/v1/cases/{case_id}")
    assert case_get.status_code == 200
    assert case_get.json()["case_id"] == case_id
