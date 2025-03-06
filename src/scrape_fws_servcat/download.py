import json
import os
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from http.client import IncompleteRead

# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def download_linked_resources(data_dir: str, data_file: str):
    with open(data_file, "r") as f:
        items = json.load(f)
    items_length = len(items)
    for i, item in enumerate(items):
        print(f"Processing item {i + 1}/{items_length}; progress: {((i + 1) / items_length) * 100:.2f}%")
        reference_type = item["referenceType"].replace(" ", "_")
        reference_id = str(item["referenceId"])
        base_dir = os.path.join(data_dir, reference_type, reference_id)

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        for j, resource in enumerate(item.get("linkedResources", [])):
            print(f"Processing resource {j + 1}/{len(item['linkedResources'])}")
            file_name = resource["fileName"]
            if base_dir is None or file_name is None:
                continue
            file_path = os.path.join(base_dir, file_name)

            if not os.path.exists(file_path):
                url = resource["url"].replace("http://", "https://")
                print(f"Downloading {url} to {file_path}")
                retries = 3
                for attempt in range(retries):
                    try:
                        response = requests.get(url, timeout=60, verify=False, stream=True)
                        response.raise_for_status()
                        with open(file_path, "wb") as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        print(f"Downloaded {file_path}")
                        time.sleep(5)
                        break
                    except (IncompleteRead, requests.exceptions.RequestException) as e:
                        print(f"Error downloading {url}: {e}")
                        if attempt < retries - 1:
                            print(f"Retrying... ({attempt + 1}/{retries})")
                            time.sleep((attempt + 4) ** 2)
                        else:
                            print(f"Failed to download {url} after {retries} attempts")
            else:
                print(f"Skipping {file_path}")


if __name__ == "__main__":
    data_file = "output.json"
    data_dir = "data"
    download_linked_resources(data_dir, data_file)
