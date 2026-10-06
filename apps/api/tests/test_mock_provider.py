"""Test AI mock provider determinism and structure."""
import asyncio
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_mock_generate_text_deterministic():
    import asyncio
    from yemenjpt.ai.mock_provider import MockModelRouter
    from yemenjpt.ai.router import Capability

    router = MockModelRouter()
    msgs = [{"role": "user", "content": "test prompt"}]
    r1 = asyncio.get_event_loop().run_until_complete(router.generate_text(Capability.SUMMARIZATION, msgs))
    r2 = asyncio.get_event_loop().run_until_complete(router.generate_text(Capability.SUMMARIZATION, msgs))
    assert r1 == r2
    assert "[SYNTHETIC]" in r1

def test_mock_extract_structured_has_entities():
    import asyncio
    from yemenjpt.ai.mock_provider import MockModelRouter

    router = MockModelRouter()
    r = asyncio.get_event_loop().run_until_complete(
        router.extract_structured("test", "entities and claims")
    )
    assert "entities" in r
    assert "claims" in r
    assert r["_synthetic"] is True

def test_mock_embed_returns_unit_vector():
    import asyncio, math
    from yemenjpt.ai.mock_provider import MockModelRouter

    router = MockModelRouter()
    vec = asyncio.get_event_loop().run_until_complete(router.embed("test text"))
    assert len(vec) == 384
    mag = math.sqrt(sum(x * x for x in vec))
    assert abs(mag - 1.0) < 1e-6

def test_mock_classify_uniform():
    import asyncio
    from yemenjpt.ai.mock_provider import MockModelRouter

    router = MockModelRouter()
    labels = ["a", "b", "c", "d"]
    r = asyncio.get_event_loop().run_until_complete(router.classify("test", labels))
    assert set(r.keys()) == set(labels)
    assert all(abs(v - 0.25) < 1e-9 for v in r.values())
