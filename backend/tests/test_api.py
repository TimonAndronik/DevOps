from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from app.db import Base, get_db  
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def prepare_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)



def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}



def test_create_and_list_tasks():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Write Dockerfile",
            "description": "Prepare backend container",
            "completed": False,
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Write Dockerfile"

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Write Dockerfile"



def test_update_task():
    create_response = client.post(
        "/tasks",
        json={"title": "Initial task", "description": "", "completed": False},
    )
    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"completed": True, "title": "Updated task"},
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["completed"] is True
    assert updated["title"] == "Updated task"



def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={"title": "Task to delete", "description": "", "completed": False},
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    assert list_response.json() == []
