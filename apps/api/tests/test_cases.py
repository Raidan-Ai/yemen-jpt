import uuid

def test_create_case(client):
    r = client.post("/api/v1/cases", json={"title": "Test Case", "research_question": "What happened?"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test Case"
    assert data["status"] == "active"
    assert "case_id" in data
    return data["case_id"]

def test_list_cases(client):
    client.post("/api/v1/cases", json={"title": "List Test Case"})
    r = client.get("/api/v1/cases")
    assert r.status_code == 200
    assert "items" in r.json()

def test_get_case(client):
    create_r = client.post("/api/v1/cases", json={"title": "Get Test"})
    case_id = create_r.json()["case_id"]
    r = client.get(f"/api/v1/cases/{case_id}")
    assert r.status_code == 200
    assert r.json()["case_id"] == case_id

def test_case_not_found(client):
    r = client.get(f"/api/v1/cases/{uuid.uuid4()}")
    assert r.status_code == 404

def test_case_timeline(client):
    create_r = client.post("/api/v1/cases", json={"title": "Timeline Test"})
    case_id = create_r.json()["case_id"]
    r = client.get(f"/api/v1/cases/{case_id}/timeline")
    assert r.status_code == 200
    assert "events" in r.json()

def test_case_entities(client):
    create_r = client.post("/api/v1/cases", json={"title": "Entities Test"})
    case_id = create_r.json()["case_id"]
    r = client.get(f"/api/v1/cases/{case_id}/entities")
    assert r.status_code == 200
    assert "entities" in r.json()

def test_case_evidence(client):
    create_r = client.post("/api/v1/cases", json={"title": "Evidence Test"})
    case_id = create_r.json()["case_id"]
    r = client.get(f"/api/v1/cases/{case_id}/evidence")
    assert r.status_code == 200
    assert "evidence" in r.json()

def test_update_case(client):
    create_r = client.post("/api/v1/cases", json={"title": "Update Test"})
    case_id = create_r.json()["case_id"]
    r = client.patch(f"/api/v1/cases/{case_id}", json={"status": "closed"})
    assert r.status_code == 200
    assert r.json()["status"] == "closed"
