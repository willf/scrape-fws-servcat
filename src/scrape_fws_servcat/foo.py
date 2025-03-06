import json

import requests


def fetch_all_items(url: str, output_file: str, top: int):
    items = []
    page = 1
    post_data = {"visibility": "public"}
    print(f"Fetching page {page}")
    initial_response = requests.post(f"{url}?top={top}&page={page}", json=post_data, timeout=60, verify=False)
    initial_response.raise_for_status()
    result = initial_response.json()
    print(f"items: {len(result['items'])}")
    print(f"Total items: {result['pageDetail']['totalCount']}")
    items.extend(result["items"])
    while result["pageDetail"]["next"]:
        page += 1
        print(f"Fetching page {page}")
        url = result["pageDetail"]["next"]
        url = url.replace("http://", "https://")
        print(f"url: {url}")
        response = requests.post(url, timeout=60, json=post_data, verify=False)
        response.raise_for_status()
        result = response.json()
        print(f"items: {len(result['items'])}")
        items.extend(result["items"])
    print(f"Total items: {len(items)}")

    with open(output_file, "w") as f:
        json.dump(items, f, indent=4)


if __name__ == "__main__":  # pragma: no cover
    url = "https://iris.fws.gov/APPS/ServCatServices/servcat/v4/rest/AdvancedSearch/Composite"
    output_file = "output.json"
    top = 500
    fetch_all_items(url, output_file, top)
