import requests

API = "https://api.crossref.org/works"

items = requests.get(API, params={"rows": 100}).json()["message"]["items"]

for it in items:
    requests.post(
        "http://localhost:8000/publications/",
        json={
            "title": it.get("title", [""])[0],
            "year": it["issued"]["date-parts"][0][0],
            "journal": it.get("container-title", [""])[0],
            "doi": it.get("DOI"),
            "abstract": {"text": it.get("abstract")},
            "metadata": it
        }
    )
