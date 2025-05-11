from datetime import datetime, timezone
import pytest

# Тест на позичення книги
def test_borrow_book(client):
    # Спочатку створюємо користувача і книгу
    user_resp = client.post("/api/users/", json={
        "first_name": "John", "last_name": "Doe", "email": "john@example.com"
    })
    book_resp = client.post("/api/books/", json={
        "title": "Test Book",
        "publication_year": 2020,
        "isbn": "1111112223334",
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    })
    user_id = user_resp.json()["id"]
    book_id = book_resp.json()["id"]

    borrow_time = datetime.now(timezone.utc).isoformat()
    response = client.post("/api/borrowed_books/", json={
        "user_id": user_id,
        "book_id": book_id,
        "borrowing_time": borrow_time,
        "return_status": "not returned"  # Return status now uses string
    })
    assert response.status_code == 201
    assert response.json()["user_id"] == user_id
    assert response.json()["book_id"] == book_id
    assert response.json()["return_status"] == "not returned"


# Повернення книги
def test_return_book(client):
    user_resp = client.post("/api/users/", json={
        "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"
    })
    book_resp = client.post("/api/books/", json={
        "title": "Book to Return",
        "publication_year": 2021,
        "isbn": "222333444345",
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    })
    borrow_time = datetime.now(timezone.utc).isoformat()
    borrow_resp = client.post("/api/borrowed_books/", json={
        "user_id": user_resp.json()["id"],
        "book_id": book_resp.json()["id"],
        "borrowing_time": borrow_time,
        "return_status": "not returned"  # Return status now uses string
    })

    borrowed_id = borrow_resp.json()["id"]
    response = client.put(f"/api/borrowed_books/{borrowed_id}", json={
        "return_status": "returned"  # Make sure return status is the correct string
    })
    assert response.status_code == 200
    assert response.json()["return_status"] == "returned"  # Ensure return status is correctly updated


# Отримання записів за користувачем
def test_get_borrowed_by_user(client):
    user = client.post("/api/users/", json={
        "first_name": "Alex", "last_name": "Smith", "email": "alex@example.com"
    }).json()
    book = client.post("/api/books/", json={
        "title": "Book A",
        "publication_year": 2022,
        "isbn": "551256667778",
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    }).json()
    borrow_time = datetime.now(timezone.utc).isoformat()
    client.post("/api/borrowed_books/", json={
        "user_id": user["id"],
        "book_id": book["id"],
        "borrowing_time": borrow_time,
        "return_status": "not returned"  # Use a string for return_status
    })

    response = client.get(f"/api/borrowed_books/user/{user['id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(b["book_id"] == book["id"] for b in response.json())


# Отримання записів за книгою
def test_get_borrowed_by_book(client):
    user = client.post("/api/users/", json={
        "first_name": "Maria", "last_name": "Stone", "email": "maria@example.com"
    }).json()
    book = client.post("/api/books/", json={
        "title": "Book B",
        "publication_year": 2023,
        "isbn": "777318889990",
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    }).json()
    borrow_time = datetime.now(timezone.utc).isoformat()
    client.post("/api/borrowed_books/", json={
        "user_id": user["id"],
        "book_id": book["id"],
        "borrowing_time": borrow_time,
        "return_status": "not returned"  # Use a string for return_status
    })

    response = client.get(f"/api/borrowed_books/book/{book['id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(b["user_id"] == user["id"] for b in response.json())


# Видалення запису про взяту книгу
def test_delete_borrowed_book(client):
    user = client.post("/api/users/", json={
        "first_name": "Nina", "last_name": "Brown", "email": "nina@example.com"
    }).json()
    book = client.post("/api/books/", json={
        "title": "Book to Delete",
        "publication_year": 2024,
        "isbn": "101310101010",
        "quantity": 1,
        "author_ids": [],
        "category_ids": []
    }).json()
    borrow_time = datetime.now(timezone.utc).isoformat()
    borrow = client.post("/api/borrowed_books/", json={
        "user_id": user["id"],
        "book_id": book["id"],
        "borrowing_time": borrow_time,
        "return_status": "not returned"  # Use a string for return_status
    }).json()

    response = client.delete(f"/api/borrowed_books/{borrow['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == borrow["id"]
