import pytest

from app import create_app
from app.helpers.sql_helper import serialize_row
from app.repositories import user_repository


@pytest.fixture()
def client(monkeypatch):
    app = create_app(
        {
            "TESTING": True,
            "AUTO_INIT_DB": False,
        }
    )

    state = {
        "next_id": 1,
        "users": {},
    }

    def clone(row):
        return serialize_row(row.copy()) if row else None

    def create_user(data):
        user_id = state["next_id"]
        state["next_id"] += 1

        row = {
            "id": user_id,
            "name": data["name"],
            "email": data["email"],
            "age": data.get("age"),
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
        }
        state["users"][user_id] = row
        return clone(row)

    def get_user_by_email(email):
        for row in state["users"].values():
            if row["email"] == email:
                return clone(row)
        return None

    def get_user_by_id(user_id):
        return clone(state["users"].get(user_id))

    def get_all_users(search=None, skip=0, limit=20):
        rows = list(state["users"].values())
        if search:
            search = search.lower()
            rows = [
                row
                for row in rows
                if search in row["name"].lower() or search in row["email"].lower()
            ]

        rows.sort(key=lambda row: row["id"], reverse=True)
        return [clone(row) for row in rows[skip : skip + limit]]

    def count_users(search=None):
        return len(get_all_users(search, skip=0, limit=9999))

    def update_user(user_id, data):
        state["users"][user_id].update(data)
        return clone(state["users"][user_id])

    def delete_user(user_id):
        return 1 if state["users"].pop(user_id, None) else 0

    monkeypatch.setattr(user_repository, "create_user", create_user)
    monkeypatch.setattr(user_repository, "get_user_by_email", get_user_by_email)
    monkeypatch.setattr(user_repository, "get_user_by_id", get_user_by_id)
    monkeypatch.setattr(user_repository, "get_all_users", get_all_users)
    monkeypatch.setattr(user_repository, "count_users", count_users)
    monkeypatch.setattr(user_repository, "update_user", update_user)
    monkeypatch.setattr(user_repository, "delete_user", delete_user)

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
