def test_submit_research(client):
    r = client.post("/api/v1/research", json={"question": "What is the status of Yemen peace talks?"})
    assert r.status_code == 200
    data = r.json()
    assert "mission_id" in data
    assert data["status"] == "pending"

def test_submit_fact_check(client):
    r = client.post("/api/v1/fact-check", json={"claim": "The UN reported X casualties in Yemen."})
    assert r.status_code == 200
    assert "mission_id" in r.json()
