import requests

BASE = "http://127.0.0.1:8000/search"

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

regex = "machine learning"
search_result = safe_request("GET", BASE, params={"regex": regex})
print("Search result:")
print(search_result)
