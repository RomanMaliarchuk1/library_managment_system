import pytest

# Створення книги
def test_create_book(client):
    response = client.post("/api/books/", json={
        "title": "Test Book",
        "publication_year": 2020,
        "isbn": "1112223334",
        "quantity": 3,
        "author_ids": [],
        "category_ids": []
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"


# Отримання списку книг
def test_read_books(client):
    response = client.get("/api/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# Отримання однієї книги
def test_read_book(client):
    # Створимо книгу
    create = client.post("/api/books/", json={
        "title": "Read Book",
        "publication_year": 2021,
        "isbn": "9876543210",
        "quantity": 2,
        "author_ids": [],
        "category_ids": []
    })
    book_id = create.json().get("id")
    assert book_id is not None, "Book ID was not returned in the response."

    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id


# Оновлення книги
def test_update_book(client):
    # Створення
    create = client.post("/api/books/", json={
        "title": "To Update",
        "publication_year": 2015,
        "isbn": "4444555566",
        "quantity": 5,
        "author_ids": [],
        "category_ids": []
    })
    book_id = create.json()["id"]

    # Оновлення
    response = client.put(f"/api/books/{book_id}", json={
        "title": "Updated Title",
        "publication_year": 2016,
        "isbn": "4444555566",
        "quantity": 10,
        "author_ids": [],
        "category_ids": []
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_search_books_by_title(client):
    client.post("/api/books/", json={
        "title": "Unique Search Title",
        "publication_year": 2000,
        "isbn": "9990001112",
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    })

    response = client.get("/api/books/", params={"title": "Unique Search Title"})
    assert response.status_code == 200
    results = response.json()
    assert any(book["title"] == "Unique Search Title" for book in results)

# Видалення книги
def test_delete_book(client):
    # Створимо книгу
    create_response = client.post("/api/books/", json={
        "title": "To Delete",
        "publication_year": 2010,
        "isbn": "7777888899",
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    })

    # Переконатися, що книга була створена
    assert create_response.status_code == 201
    book_id = create_response.json()["id"]
    assert book_id is not None

    # Видалити книгу
    delete_response = client.delete(f"/api/books/{book_id}")
    assert delete_response.status_code == 200

    # Перевірити, що книга була видалена
    get_after_delete = client.get(f"/api/books/{book_id}")
    assert get_after_delete.status_code == 404

def test_create_book_with_duplicate_isbn(client):
    # Створення першої книги
    create_response_1 = client.post("/api/books/", json={
        "title": "Duplicate ISBN Book",
        "publication_year": 2022,
        "isbn": "1234567890",  # Унікальний ISBN
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    })
    assert create_response_1.status_code == 201

    # Створення другої книги з тим самим ISBN
    create_response_2 = client.post("/api/books/", json={
        "title": "Duplicate ISBN Book Again",
        "publication_year": 2023,
        "isbn": "1234567890",  # Такий же ISBN
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    })

    assert create_response_2.status_code == 400
    assert "ISBN" in create_response_2.json()["detail"]


def test_update_non_existent_book(client):
    non_existent_book_id = 99999999  # Випадковий ID, який не існує в базі

    update_response = client.put(f"/api/books/{non_existent_book_id}", json={
        "title": "Non Existent Book",
        "publication_year": 2025,
        "isbn": "3334445556",
        "quantity": 10,
        "author_ids": [],
        "category_ids": []
    })

    # Перевірка, що отримали помилку 404, бо книги не існує
    assert update_response.status_code == 404
    assert "detail" in update_response.json()

def test_read_non_existent_book(client):
    non_existent_book_id = 99999999  # Випадковий ID, який не існує в базі

    response = client.get(f"/api/books/{non_existent_book_id}")
    # Перевірка, що отримали помилку 404, бо книги не існує
    assert response.status_code == 404
    assert "detail" in response.json()

def test_get_all_books(client):
    # Створимо кілька книг
    client.post("/api/books/", json={
        "title": "Book 1",
        "publication_year": 2021,
        "isbn": "1234509876",
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    })
    client.post("/api/books/", json={
        "title": "Book 2",
        "publication_year": 2022,
        "isbn": "9876543211",
        "quantity": 2,
        "author_ids": [],
        "category_ids": []
    })

    # Отримання списку всіх книг
    response = client.get("/api/books/")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    assert len(books) > 0