import requests
import json
from datetime import datetime, timedelta

# API Configuration
API_BASE_URL = "http://localhost:5000/api"
TOKEN = None

def print_response(response, title):
    print(f"\n{title}")
    print("-" * 50)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_registration():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123456",
        "department": "computer"
    }
    response = requests.post(f"{API_BASE_URL}/auth/register", json=data)
    print_response(response, "Testing Registration")
    return response.ok

def test_login():
    data = {
        "username": "testuser",
        "password": "Test123456"
    }
    response = requests.post(f"{API_BASE_URL}/auth/login", json=data)
    print_response(response, "Testing Login")
    if response.ok:
        global TOKEN
        TOKEN = response.json()["access_token"]
    return response.ok

def test_create_post():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {
        "title": "Test Post",
        "content": "This is a test post content",
        "category": "announcement"
    }
    response = requests.post(f"{API_BASE_URL}/posts", headers=headers, json=data)
    print_response(response, "Testing Post Creation")
    return response.json() if response.ok else None

def test_get_posts():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{API_BASE_URL}/posts", headers=headers)
    print_response(response, "Testing Get Posts")
    return response.ok

def test_create_event():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {
        "title": "Test Event",
        "description": "This is a test event",
        "date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location"
    }
    response = requests.post(f"{API_BASE_URL}/events", headers=headers, json=data)
    print_response(response, "Testing Event Creation")
    return response.json() if response.ok else None

def test_get_events():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{API_BASE_URL}/events", headers=headers)
    print_response(response, "Testing Get Events")
    return response.ok

def test_get_stats():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{API_BASE_URL}/stats", headers=headers)
    print_response(response, "Testing Get Stats")
    return response.ok

def test_update_post(post_id):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {
        "title": "Updated Test Post",
        "content": "This is an updated test post content",
        "category": "announcement"
    }
    response = requests.put(f"{API_BASE_URL}/posts/{post_id}", headers=headers, json=data)
    print_response(response, "Testing Post Update")
    return response.ok

def test_delete_post(post_id):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.delete(f"{API_BASE_URL}/posts/{post_id}", headers=headers)
    print_response(response, "Testing Post Deletion")
    return response.ok

def test_delete_event(event_id):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.delete(f"{API_BASE_URL}/events/{event_id}", headers=headers)
    print_response(response, "Testing Event Deletion")
    return response.ok

def main():
    print("Starting API Tests...")
    
    # Test registration
    if not test_registration():
        print("Registration failed. Stopping tests.")
        return
    
    # Test login
    if not test_login():
        print("Login failed. Stopping tests.")
        return
    
    # Test post operations
    post = test_create_post()
    if post:
        test_get_posts()
        test_update_post(post["id"])
        test_delete_post(post["id"])
    
    # Test event operations
    event = test_create_event()
    if event:
        test_get_events()
        test_delete_event(event["id"])
    
    # Test stats
    test_get_stats()
    
    print("\nAPI Testing Complete!")

if __name__ == "__main__":
    main() 