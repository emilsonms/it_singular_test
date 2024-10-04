from fastapi.testclient import TestClient
from jose import jwt
from src.main import app
from src.controllers.auth import SECRET_KEY, ALGORITHM


client = TestClient(app)

def create_jwt_token(username: str):
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)


def test_admin_route_no_token():
    response = client.get("/admin")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_admin_route_with_user_token():
    token = create_jwt_token("emilson")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin", headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "You do not have the necessary permissions"}


def test_admin_route_with_admin_token():
    token = create_jwt_token("admin")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == "admin"
    assert data["data"]["role"] == "admin"
