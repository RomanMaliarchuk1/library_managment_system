import pytest

# Створення користувача
def test_create_user(client):
    response = client.post("/api/users/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "john.doe@example.com"

# Отримання списку користувачів
def test_read_users(client):
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Отримання одного користувача
def test_read_user(client):
    create_response = client.post("/api/users/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    })
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == user_id

# Оновлення користувача
def test_update_user(client):
    create_response = client.post("/api/users/", json={
        "first_name": "Bob",
        "last_name": "Builder",
        "email": "bob@example.com"
    })
    user_id = create_response.json()["id"]

    update_response = client.put(f"/api/users/{user_id}", json={
        "first_name": "Bobby",
        "last_name": "Builder",
        "email": "bob@example.com"
    })
    assert update_response.status_code == 200
    assert update_response.json()["first_name"] == "Bobby"

# Видалення користувача
def test_delete_user(client):
    create_response = client.post("/api/users/", json={
        "first_name": "Charlie",
        "last_name": "Chaplin",
        "email": "charlie@example.com"
    })
    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/users/{user_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404