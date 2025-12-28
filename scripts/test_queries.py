import requests

BASE_QUERIES = "http://127.0.0.1:8000/queries"
BASE_SEARCH = "http://127.0.0.1:8000/search"

def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {r.status_code} for {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError:
        print(f"Failed to decode JSON from {url}")
        return None

def safe_put(url, params=None):
    try:
        r = requests.put(url, params=params)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {r.status_code} for {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError:
        print(f"Failed to decode JSON from {url}")
        return None

# --- 1. SELECT ... WHERE ---
print("\n--- 1. SELECT ... WHERE ---")
where_params = {"year": 2025, "journal": "Aloha International Journal of Management Advancement"}
where_result = safe_get(BASE_QUERIES + "/where", params=where_params)
if where_result:
    print(f"Query: year={where_params['year']}, journal={where_params['journal']}")
    print(f"Returned {len(where_result)} records")
    for r in where_result:
        print(r)
else:
    print("No records returned or query failed")

# --- 2. JOIN ---
print("\n--- 2. JOIN ---")
join_result = safe_get(BASE_QUERIES + "/join")
if join_result:
    print(f"Returned {len(join_result)} records")
    for pub, author in join_result:
        print(pub, author)
else:
    print("No records returned or query failed")

# --- 3. UPDATE with non-trivial condition ---
print("\n--- 3. UPDATE with non-trivial condition ---")
update_params = {"prefix": "https://doi.org/"}
update_result = safe_put(BASE_QUERIES + "/update_doi", params=update_params)
print(update_result if update_result else "Update failed")

# --- 4. GROUP BY year ---
print("\n--- 4. GROUP BY year ---")
group_by_result = safe_get(BASE_QUERIES + "/group_by_year")
if group_by_result:
    for year, count in group_by_result:
        print(f"Year: {year}, Count: {count}")
else:
    print("Group by query failed or returned no results")

# --- 5. SORT ---
print("\n--- 5. SORT ---")
sort_params = {"desc": True}
sort_result = safe_get(BASE_QUERIES + "/sorted", params=sort_params)
if sort_result:
    print(f"Returned {len(sort_result)} records")
    for r in sort_result[:10]:  # print only first 10 for brevity
        print(r)
else:
    print("Sort query failed or returned no results")

# --- 6. SEARCH (full-text in abstract) ---
print("\n--- 6. SEARCH in abstracts ---")
regex = "machine learning"
search_result = safe_get(BASE_SEARCH + "/", params={"regex": regex})
if search_result:
    print(f"Returned {len(search_result)} records")
    for r in search_result[:10]:  # print first 10 for brevity
        print(r)
else:
    print("Search query failed or returned no results")
