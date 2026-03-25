from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task_success():
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"


def test_create_task_failure():
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_get_task_not_found():
    response = client.get("/tasks/11111111-1111-1111-1111-111111111111")
    assert response.status_code == 404


def test_list_tasks():
    response = client.get("/tasks?page=1&page_size=5")
    assert response.status_code == 200


def test_update_task():
    res = client.post("/tasks", json={"title": "Update me"})
    task_id = res.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "done"})
    assert response.status_code == 200


def test_delete_task():
    res = client.post("/tasks", json={"title": "Delete me"})
    task_id = res.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
