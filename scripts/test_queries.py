import requests

BASE = "http://127.0.0.1:8000/queries"

def safe_request(method, url, **kwargs):
    r = requests.request(method, url, **kwargs)
    if r.status_code == 200:
        try:
            return r.json()
        except Exception:
            print(f"Warning: Response not JSON. Content:\n{r.text}")
            return None
    else:
        print(f"Error: HTTP {r.status_code} for {url}")
        print(r.text)
        return None

# WHERE
print("WHERE query:")
where_result = safe_request("GET", BASE + "/where", params={"year": 2020, "journal": "Nature"})
print(where_result)

# JOIN
print("JOIN query:")
join_result = safe_request("GET", BASE + "/join")
print(join_result)

# GROUP BY
print("GROUP BY query:")
group_result = safe_request("GET", BASE + "/group_by_year")
print(group_result)

# UPDATE
print("UPDATE query:")
update_result = safe_request("PUT", BASE + "/update_doi", params={"prefix": "https://doi.org/"})
print(update_result)

# SORT
print("SORT query:")
sort_result = safe_request("GET", BASE + "/sorted", params={"desc": True})
print(sort_result)
