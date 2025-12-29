import requests

API = "https://api.crossref.org/works"
items = requests.get(API, params={"rows": 300}).json()["message"]["items"]

for it in items:
    authors = it.get("author", [])
    author_name = None
    if authors:
        import requests

        API = "https://api.crossref.org/works"
        items = requests.get(API, params={"rows": 300}).json()["message"]["items"]

        for it in items:
            authors = it.get("author", [])
            authors_payload = []
            if authors:
                a = authors[0]
                authors_payload = [
                    {
                        "given": a.get("given", ""),
                        "family": a.get("family", ""),
                        "affiliation": a.get("affiliation", []),
                    }
                ]

            requests.post(
                "http://localhost:8000/publications/",
                json={
                    "title": it.get("title", [""])[0],
                    "year": it["issued"]["date-parts"][0][0],
                    "journal": it.get("container-title", [""])[0],
                    "doi": it.get("DOI"),
                    "abstract": {"text": it.get("abstract")},
                    "metadata_json": it,
                    "authors": authors_payload
                }
            )
