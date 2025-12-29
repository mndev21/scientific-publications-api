import requests
import re
import json

BASE = "http://127.0.0.1:8000/queries"


def print_block(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# 1. SELECT ... WHERE (multiple conditions)
print_block("1. SELECT ... WHERE (multiple conditions)")

params = {
    "year": 2020,
    "journal": "Journal"
}

r = requests.get(f"{BASE}/where", params=params)
if r.status_code == 200:
    data = r.json()
    print(f"Returned {len(data)} records")
    for row in data[:5]:
        print({
            "id": row["id"],
            "year": row["year"],
            "journal": row["journal"],
            "doi": row["doi"]
        })
else:
    print("Error:", r.text)


# 2. JOIN publications + authors
print_block("2. JOIN publications + authors")

r = requests.get(f"{BASE}/join")
if r.status_code == 200:
    data = r.json()
    print(f"Returned {len(data)} records")
    for row in data[:-1]:
        print({
            "title": row["title"],
            "year": row["year"],
            "journal": row["journal"],
            "author": row["author"]
        })
else:
    print("Error:", r.text)


# 3. UPDATE with non-trivial condition
print_block("3. UPDATE with non-trivial condition")

r = requests.put(f"{BASE}/update_doi")
if r.status_code == 200:
    print("Update result:", r.json())
else:
    print("Error:", r.text)


# 4. GROUP BY year
print_block("4. GROUP BY year")

r = requests.get(f"{BASE}/group_by_year")
if r.status_code == 200:
    data = r.json()
    for row in data:
        print(f"Year {row['year']}: {row['count']} publications")
else:
    print("Error:", r.text)


# 5. SORT (ORDER BY)
print_block("5. SORT by year DESC")

params = {
    "desc": True
}

r = requests.get(f"{BASE}/sorted", params=params)
if r.status_code == 200:
    data = r.json()
    print(f"Returned {len(data)} records")
    for row in data[:5]:
        print({
            "title": row["title"],
            "journal": row["journal"],
            "year": row["year"]
        })
else:
    print("Error:", r.text)


# 6. Full-text search on JSONB metadata_json using pg_trgm + GIN
print_block("6. Full-text search on JSONB metadata_json using pg_trgm + GIN")

# Provide a POSIX/psql-style regex for searching the JSONB text (server uses ~* operator)
params = {
    "query": "Aloha International Journal of Management Advancement"  # replace with regex or text you want to search
}

r = requests.get(f"{BASE}/search_metadata", params=params)
if r.status_code == 200:
    data = r.json()
    print(f"Returned {len(data)} records matching regex: {params['query']}")
    pattern = re.compile(params['query'], re.IGNORECASE)

    for row in data:
        # convert metadata_json to text for client-side matching and extraction
        mj_text = json.dumps(row.get("metadata_json", {}))
        matches = pattern.findall(mj_text)
        # Only show rows where we found matches (server already filtered, but this trims output)
        if not matches:
            continue

        print({
            "id": row["id"],
            "title": row["title"],
            "matches": matches[:10]  # show up to 10 match snippets
        })
else:
    print("Error:", r.text)




# r = requests.get(f"{BASE}/where", params={"limit": 5, "offset": 0})
# data = r.json()
# print(f"Returned {len(data)} records")
# for row in data:
    # print(row)
# 