from fastapi.testclient import TestClient
from jose import jwt
from src.main import app
from src.controllers.auth import SECRET_KEY, ALGORITHM


client = TestClient(app)


def create_jwt_token(username: str):
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)


def test_user_route_no_token():
    response = client.get("/user")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_user_route_with_user_token():
    token = create_jwt_token("emilson")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "emilson"
    assert data["data"]["role"] == "user"


def test_user_route_with_admin_token():
    token = create_jwt_token("admin")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "admin"
    assert data["data"]["role"] == "admin"
