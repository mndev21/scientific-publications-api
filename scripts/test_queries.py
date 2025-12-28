import requests

BASE = "http://127.0.0.1:8000/queries"

# WHERE
print("WHERE query:")
r = requests.get(BASE + "/where", params={"year": 2020, "journal": "Nature"})
print(r.json())

# JOIN
print("JOIN query:")
r = requests.get(BASE + "/join")
print(r.json())

# GROUP BY
print("GROUP BY query:")
r = requests.get(BASE + "/group_by_year")
print(r.json())

# UPDATE
print("UPDATE query:")
r = requests.put(BASE + "/update_doi", params={"prefix": "https://doi.org/"})
print(r.json())

# SORT
print("SORT query:")
r = requests.get(BASE + "/sorted", params={"desc": True})
print(r.json())
