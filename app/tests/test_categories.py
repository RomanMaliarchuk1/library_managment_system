import pytest

# Створення категорії
def test_create_category(client):
    response = client.post("/api/categories/", json={
        "category_name": "Science Fiction",
        "description": "Fictional works based on scientific concepts"
    })
    assert response.status_code == 201
    assert response.json()["category_name"] == "Science Fiction"

# Отримання списку категорій
def test_read_categories(client):
    response = client.get("/api/categories/")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)

# Отримання однієї категорії
def test_read_category(client):
    # Створимо категорію
    create_response = client.post("/api/categories/", json={
        "category_name": "Fantasy",
        "description": "Magical and supernatural themes"
    })
    category_id = create_response.json()["id"]

    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["id"] == category_id

# Оновлення категорії
def test_update_category(client):
    create_response = client.post("/api/categories/", json={
        "category_name": "Horror",
        "description": "Scary stories"
    })
    category_id = create_response.json()["id"]

    update_response = client.put(f"/api/categories/{category_id}", json={
        "category_name": "Psychological Horror",
        "description": "Horror focusing on the mental state"
    })
    assert update_response.status_code == 200
    assert update_response.json()["category_name"] == "Psychological Horror"

# Видалення категорії
def test_delete_category(client):
    create_response = client.post("/api/categories/", json={
        "category_name": "To Delete",
        "description": "Temporary"
    })
    category_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/categories/{category_id}")
    assert delete_response.status_code == 200

    # Перевіримо, що категорія була видалена
    get_after_delete = client.get(f"/api/categories/{category_id}")
    assert get_after_delete.status_code == 404
