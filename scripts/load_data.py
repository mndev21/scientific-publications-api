import requests

API = "https://api.crossref.org/works"
LOCAL_API = "http://127.0.0.1:8000/publications/"

items = requests.get(API, params={"rows": 100}).json()["message"]["items"]

for it in items:
    authors = it.get("author", [])
    author_name = None

    if authors:
        given = authors[0].get("given", "")
        family = authors[0].get("family", "")
        author_name = f"{given} {family}".strip()

    payload = {
        "title": it.get("title", [""])[0],
        "year": it["issued"]["date-parts"][0][0],
        "journal": it.get("container-title", [""])[0],
        "doi": it.get("DOI"),
        "abstract": {"text": it.get("abstract")},
        "metadata_json": it,
    }

    if author_name:
        payload["author"] = {"name": author_name}

    requests.post(LOCAL_API, json=payload)
