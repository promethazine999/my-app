from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

users = [
    {'id': 1, 'name': 'Ivan Ivanov', 'email': 'i.i.ivanov@mail.com'},
    {'id': 2, 'name': 'Petr Petrov', 'email': 'p.p.petrov@mail.com'},
]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': 'unknown@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    new_user_data = {"name": "Alex Smith", "email": "alex.smith@mail.com"}
    response = client.post("/api/v1/user", json=new_user_data)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

def test_create_user_with_invalid_email():
    duplicated = {"name": "New Ivan", "email": users[0]['email']}
    response = client.post("/api/v1/user", json=duplicated)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    response = client.delete("/api/v1/user", params={'email': users[1]['email']})
    assert response.status_code == 204
