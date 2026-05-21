from uuid import uuid4


def test_create_and_list_tasks(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Ship portfolio API", "description": "Make it polished"},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Ship portfolio API"
    assert created["status"] == "todo"

    list_response = client.get("/api/v1/tasks")

    assert list_response.status_code == 200
    assert list_response.json() == [created]
def test_update_task(client):
    created = client.post("/api/v1/tasks", json={"title": "Draft"}).json()

    response = client.put(
        f"/api/v1/tasks/{created['id']}",
        json={"title": "Refined", "description": "Ready", "status": "done"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Refined"
    assert response.json()["description"] == "Ready"
    assert response.json()["status"] == "done"
