import requests

response = requests.post(
    "http://10.247.5.175:5000/prediksi/1"
)

print(response.json())
