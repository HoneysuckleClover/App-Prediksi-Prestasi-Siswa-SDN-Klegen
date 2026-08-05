import requests

url = "http://10.247.5.175:5000/login"

data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post(url, json=data)

print(response.json())
