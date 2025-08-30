import requests
from requests.auth import HTTPBasicAuth

url = "http://127.0.0.1:8000/api/loan/request/"
data = {
    "client_id": "0001",
    "location": {"lat": -25.9992, "long": 28.1286}
}

# If you're using Basic Auth
response = requests.post(url, json=data, auth=HTTPBasicAuth('username', 'password'))

# If you're using Token Auth, get a token first
# First get a token
login_url = "http://127.0.0.1:8000/api/token/"
login_data = {"username": "your_username", "password": "your_password"}
token_response = requests.post(login_url, json=login_data)
token = token_response.json().get("access")

# Then use the token
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(url, json=data, headers=headers)

print("Status:", response.status_code)
print("Response:", response.json())