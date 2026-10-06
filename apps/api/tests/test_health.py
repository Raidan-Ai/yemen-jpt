def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "timestamp" in data

def test_readiness(client):
    r = client.get("/health/readiness")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"
