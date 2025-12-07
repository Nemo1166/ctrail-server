"""Test leaderboard API endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.database import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_leaderboard.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_submit_score():
    """Test submit score endpoint."""
    response = client.post(
        "/api/leaderboard/submit",
        json={
            "player_id": "test_player_1",
            "score": 1000,
            "timestamp": 1701936000
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "data" in data
    assert data["data"]["rank"] >= 1
    assert data["data"]["best_score"] == 1000


def test_get_leaderboard():
    """Test get leaderboard endpoint."""
    # Submit a few scores first
    client.post("/api/leaderboard/submit", json={"player_id": "player_1", "score": 1500})
    client.post("/api/leaderboard/submit", json={"player_id": "player_2", "score": 2000})
    
    response = client.get("/api/leaderboard?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "data" in data
    assert "entries" in data["data"]
    assert data["data"]["total"] >= 2


def test_get_player_rank():
    """Test get player rank endpoint."""
    # Submit a score first
    client.post("/api/leaderboard/submit", json={"player_id": "test_player_2", "score": 3000})
    
    response = client.get("/api/leaderboard/player/test_player_2")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["player_id"] == "test_player_2"
    assert data["data"]["score"] == 3000


def test_get_player_rank_not_found():
    """Test get player rank for non-existent player."""
    response = client.get("/api/leaderboard/player/nonexistent_player")
    assert response.status_code == 404
