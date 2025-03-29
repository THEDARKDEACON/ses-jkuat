import requests

def check_server():
    try:
        response = requests.get("http://localhost:5000/")
        print(f"Server Status Code: {response.status_code}")
        print(f"Server Response: {response.text[:500]}...")  # Print first 500 characters
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it's running on http://localhost:5000")

if __name__ == "__main__":
    check_server() 