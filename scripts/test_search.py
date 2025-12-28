import requests

BASE = "http://127.0.0.1:8000/search"

regex = "machine learning"
r = requests.get(BASE, params={"regex": regex})
print(r.json())
