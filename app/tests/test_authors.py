import pytest

# Створення автора
def test_create_author(client):
    response = client.post("/api/authors/", json={
        "first_name": "John",
        "second_name": "Doe",
        "biography": "An unknown author"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["second_name"] == "Doe"

# Отримання списку авторів
def test_read_authors(client):
    # Створюємо одного автора
    client.post("/api/authors/", json={
        "first_name": "Jane",
        "second_name": "Smith",
        "biography": "Author of many books"
    })
    response = client.get("/api/authors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Отримання одного автора
def test_read_author(client):
    create = client.post("/api/authors/", json={
        "first_name": "Alice",
        "second_name": "Walker",
        "biography": "Biography"
    })
    author_id = create.json()["id"]

    response = client.get(f"/api/authors/{author_id}")
    assert response.status_code == 200
    assert response.json()["id"] == author_id

# Оновлення автора
def test_update_author(client):
    create = client.post("/api/authors/", json={
        "first_name": "Update",
        "second_name": "Test",
        "biography": "Before update"
    })
    author_id = create.json()["id"]

    response = client.put(f"/api/authors/{author_id}", json={
        "first_name": "Updated",
        "second_name": "Tested",
        "biography": "After update"
    })

    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"
    assert response.json()["biography"] == "After update"

# Видалення автора без книг
def test_delete_author(client):
    create = client.post("/api/authors/", json={
        "first_name": "To",
        "second_name": "Delete",
        "biography": "No books"
    })
    author_id = create.json()["id"]

    delete_response = client.delete(f"/api/authors/{author_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/api/authors/{author_id}")
    assert get_response.status_code == 404

# Видалення автора з книгами (повинно повернути 400)
def test_delete_author_with_books(client):
    # Створимо автора
    author = client.post("/api/authors/", json={
        "first_name": "Linked",
        "second_name": "Author",
        "biography": "Will be linked to a book"
    }).json()
    author_id = author["id"]

    # Створимо книгу з цим автором
    book = client.post("/api/books/", json={
        "title": "Linked Book",
        "publication_year": 2020,
        "isbn": "5556667778",
        "quantity": 1,
        "author_ids": [author_id],
        "category_ids": []
    })
    assert book.status_code == 201

    # Спроба видалити автора
    delete_response = client.delete(f"/api/authors/{author_id}")
    assert delete_response.status_code == 400
    assert "associated books" in delete_response.json()["detail"]

# Отримання неіснуючого автора
def test_read_nonexistent_author(client):
    response = client.get("/api/authors/999999")
    assert response.status_code == 404

# Оновлення неіснуючого автора
def test_update_nonexistent_author(client):
    response = client.put("/api/authors/999999", json={
        "first_name": "Ghost",
        "second_name": "Writer",
        "biography": "No one"
    })
    assert response.status_code == 404

# Видалення неіснуючого автора
def test_delete_nonexistent_author(client):
    response = client.delete("/api/authors/999999")
    assert response.status_code == 404