from types import SimpleNamespace

import mongomock
import pytest

from app import create_app
from app.repositories import user_repository


@pytest.fixture()
def client(monkeypatch):
    app = create_app(
        {
            "TESTING": True,
            "MONGO_URI": "mongodb://localhost:27017/flask_mongo_crud_test",
        }
    )

    fake_mongo = SimpleNamespace(db=mongomock.MongoClient().flask_mongo_crud_test)
    fake_mongo.db.users.create_index("email", unique=True)
    monkeypatch.setattr(user_repository, "mongo", fake_mongo)

    return app.test_client()


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["success"] is True


def test_user_crud_flow(client):
    malformed_response = client.post(
        "/api/v1/users",
        data='{"name":',
        content_type="application/json",
    )
    assert malformed_response.status_code == 400
    assert malformed_response.get_json()["message"] == "Invalid JSON body"

    invalid_response = client.post("/api/v1/users", json={"email": "bad-email"})
    assert invalid_response.status_code == 400

    create_response = client.post(
        "/api/v1/users",
        json={"name": "Div", "email": "DIV@example.com", "age": 25},
    )
    create_body = create_response.get_json()

    assert create_response.status_code == 201
    assert create_body["data"]["email"] == "div@example.com"

    user_id = create_body["data"]["id"]

    duplicate_response = client.post(
        "/api/v1/users",
        json={"name": "Div 2", "email": "div@example.com", "age": 26},
    )
    assert duplicate_response.status_code == 409

    list_response = client.get("/api/v1/users")
    list_body = list_response.get_json()

    assert list_response.status_code == 200
    assert list_body["meta"]["total"] == 1
    assert list_body["data"][0]["id"] == user_id

    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["data"]["name"] == "Div"

    update_response = client.put(
        f"/api/v1/users/{user_id}",
        json={"name": "Div Updated", "age": 26},
    )
    update_body = update_response.get_json()

    assert update_response.status_code == 200
    assert update_body["data"]["name"] == "Div Updated"
    assert update_body["data"]["age"] == 26

    delete_response = client.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 200

    get_deleted_response = client.get(f"/api/v1/users/{user_id}")
    assert get_deleted_response.status_code == 404
