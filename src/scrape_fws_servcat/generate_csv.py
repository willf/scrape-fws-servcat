import csv
import json
import uuid
from pathlib import Path

from scrape_fws_servcat.utils import humanize_bytes


def generate_csv(data_file: str, output_dir: str = "."):
    """
    Generate two CSV files from the JSON data:
    1. references.csv - containing all reference information
    2. linked_resources.csv - containing all linked resources with a join column (referenceId)

    Args:
        data_file: Path to the JSON file containing the references
        output_dir: Directory where the CSV files should be saved
    """
    with open(data_file, "r") as f:
        items = json.load(f)

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Define paths for output files
    references_file = Path(output_dir) / "references.csv"
    resources_file = Path(output_dir) / "linked_resources.csv"

    # Generate references.csv
    reference_fields = [
        "referenceId",
        "referenceType",
        "lifecycle",
        "visibility",
        "fileCount",
        "fileAccess",
        "title",
        "citation",
        "newestVersion",
    ]

    with open(references_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reference_fields)
        writer.writeheader()

        for item in items:
            # Extract only the fields we want
            row = {field: item.get(field, "") for field in reference_fields}
            writer.writerow(row)

    # Generate linked_resources.csv
    resource_fields = [
        *reference_fields,
        "resourceId",
        "referenceId",
        "enumeration",
        "resourceType",
        "url",
        "description",
        "fileType",
        "fileName",
        "fileSize",
        "humanizedSize",
    ]

    with open(resources_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=resource_fields)
        writer.writeheader()

        for item in items:
            reference_id = item.get("referenceId", uuid.uuid4())

            for i, resource in enumerate(item.get("linkedResources", [])):
                row = {
                    "resourceId": resource.get("resourceId", uuid.uuid4()),
                    "referenceId": reference_id,
                    "enumeration": i + 1,
                    "referenceType": item.get("referenceType", ""),
                    "lifecycle": item.get("lifecycle", ""),
                    "visibility": item.get("visibility", ""),
                    "fileCount": item.get("fileCount", ""),
                    "fileAccess": item.get("fileAccess", ""),
                    "title": item.get("title", ""),
                    "citation": item.get("citation", ""),
                    "newestVersion": item.get("newestVersion", ""),
                    "resourceType": resource.get("resourceType", ""),
                    "url": resource.get("url", ""),
                    "description": resource.get("description", ""),
                    "fileType": resource.get("type", ""),
                    "fileName": resource.get("fileName", ""),
                    "fileSize": resource.get("fileSize", ""),
                    "humanizedSize": "",
                }

                # Add humanized file size
                file_size = resource.get("fileSize", 0)
                if file_size and file_size != "":
                    try:
                        row["humanizedSize"] = humanize_bytes(int(file_size))
                    except (ValueError, TypeError):
                        row["humanizedSize"] = ""
                else:
                    row["humanizedSize"] = ""

                writer.writerow(row)

    print(f"CSV files generated and saved to {references_file} and {resources_file}")


if __name__ == "__main__":
    data_file = "output.json"
    output_dir = "."
    generate_csv(data_file, output_dir)
