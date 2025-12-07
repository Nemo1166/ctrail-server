"""Simple API test script."""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())

def test_submit_score():
    """Test submit score."""
    data = {
        "player_id": "player_001",
        "score": 5000
    }
    response = requests.post(f"{BASE_URL}/api/leaderboard/submit", json=data)
    print("Submit Score:", response.json())

def test_get_leaderboard():
    """Test get leaderboard."""
    response = requests.get(f"{BASE_URL}/api/leaderboard?limit=10")
    print("Leaderboard:", json.dumps(response.json(), indent=2))

def test_get_player_rank():
    """Test get player rank."""
    response = requests.get(f"{BASE_URL}/api/leaderboard/player/player_001")
    print("Player Rank:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Game Leaderboard API")
    print("=" * 50)
    
    print("\n1. Testing Health Check...")
    test_health()
    
    print("\n2. Testing Submit Score...")
    test_submit_score()
    
    print("\n3. Testing Get Leaderboard...")
    test_get_leaderboard()
    
    print("\n4. Testing Get Player Rank...")
    test_get_player_rank()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
