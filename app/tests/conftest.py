import os
import subprocess
import pytest
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session", autouse=True)
def set_test_environment():
    os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@db:5432/library_test"  # або шлях до тестової БД

    yield


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"], check=True)

    yield

    subprocess.run(["alembic", "downgrade", "base"], check=True)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
