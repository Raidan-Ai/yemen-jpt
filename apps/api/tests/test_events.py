def test_create_event(client):
    r = client.post("/api/v1/events", json={"event_type": "test.event", "source_id": "test_source", "payload": {"key": "value"}})
    assert r.status_code == 201
    data = r.json()
    assert data["event_type"] == "test.event"
    assert "event_id" in data
    assert data["confidence"]["label"] == "unknown"

def test_get_event(client):
    create_r = client.post("/api/v1/events", json={"event_type": "get.test", "source_id": "src1"})
    event_id = create_r.json()["event_id"]
    r = client.get(f"/api/v1/events/{event_id}")
    assert r.status_code == 200
    assert r.json()["event_id"] == event_id
