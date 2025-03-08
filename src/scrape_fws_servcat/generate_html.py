import json
from datetime import datetime

from scrape_fws_servcat.utils import humanize_bytes


def generate_html(data_file: str, output_file: str):
    """
    Generate a static HTML file from the JSON data.

    Args:
        data_file: Path to the JSON file containing the references
        output_file: Path where the HTML file should be saved
    """
    with open(data_file, "r") as f:
        items = json.load(f)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>US Fish and Wildlife Services ServCat References</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }
        .reference {
            margin-bottom: 30px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .reference h2 {
            margin-top: 0;
            color: #3498db;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .reference-details {
            margin-bottom: 15px;
        }
        .reference-details p {
            margin: 5px 0;
        }
        .resources {
            margin-top: 10px;
        }
        .resource {
            background-color: #fff;
            border: 1px solid #eee;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 3px;
        }
        .resource h3 {
            margin-top: 0;
            color: #2c3e50;
            font-size: 16px;
        }
        .metadata {
            font-size: 0.9em;
            color: #666;
        }
        .resource-link {
            display: inline-block;
            margin-top: 10px;
            background-color: #3498db;
            color: white;
            padding: 5px 10px;
            text-decoration: none;
            border-radius: 3px;
        }
        .resource-link:hover {
            background-color: #2980b9;
        }
        .gen-link {
            color: #3498db;
            text-decoration: none;
        }
        .gen-link:hover {
            text-decoration: underline;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 0.9em;
            color: #777;
        }
        .search-bar {
            margin-bottom: 0;
            margin-right: 10px;
            flex-grow: 1;
            max-width: 800px;
        }
        .search-bar input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .made-by {
            width: 100%;
            text-align: center;
            padding: 10px 0;
        }
        .button {
            background-color: #3498db;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 0 5px;
        }
        .button:hover {
            background-color: #2980b9;
        }
        .clear-button {
            background-color: #e74c3c;
        }
        .clear-button:hover {
            background-color: #c0392b;
        }
        .search-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        /* Spinner styles */
        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top-color: #3498db;
            animation: spin 1s ease-in-out infinite;
            margin-left: 10px;
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }

        .page-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .page-spinner {
            width: 60px;
            height: 60px;
            border: 5px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top-color: #3498db;
            animation: spin 1s ease-in-out infinite;
        }

        #resultCount {
            margin-left: 10px;
            font-style: italic;
        }
    </style>
    <script>
        function searchReferences() {
            // Show spinner
            document.getElementById('searchSpinner').style.display = 'block';

            setTimeout(() => {
                const searchValue = document.getElementById('searchInput').value.toLowerCase();
                const references = document.querySelectorAll('.reference');

                let matchCount = 0;
                for (const ref of references) {
                    const title = ref.getAttribute('data-title').toLowerCase();
                    const type = ref.getAttribute('data-type').toLowerCase();
                    const abstract = ref.getAttribute('data-abstract').toLowerCase();

                    if (title.includes(searchValue) || type.includes(searchValue) || abstract.includes(searchValue)) {
                        ref.style.display = 'block';
                        matchCount++;
                    } else {
                        ref.style.display = 'none';
                    }
                }

                // Hide spinner
                document.getElementById('searchSpinner').style.display = 'none';

                // Update results count
                document.getElementById('resultCount').textContent = `${matchCount} matches found`;
            }, 50); // Small delay to ensure spinner shows
        }

        function clearSearch() {
            document.getElementById('searchInput').value = '';
            document.getElementById('resultCount').textContent = '';
            const references = document.querySelectorAll('.reference');

            for (const ref of references) {
                ref.style.display = 'block';
            }
        }

        function initSearchListener() {
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.addEventListener('keypress', function(event) {
                    if (event.key === 'Enter') {
                        searchReferences();
                    }
                });
            }
        }

        window.onload = function() {
            initSearchListener();

            // Remove page loading overlay
            setTimeout(() => {
                document.getElementById('pageLoadOverlay').style.display = 'none';
            }, 500);
        };
    </script>
</head>
<body>
    <!-- Page loading overlay with spinner -->
    <div id="pageLoadOverlay" class="page-overlay">
        <div class="page-spinner"></div>
    </div>

    <div class="container">
        <h1>US Fish and Wildlife Services ServCat Catalog</h1>
        <div class="made-by">
                <p>Made with ❤️ by <a href="https://envirodatagov.org/" class="gen-link">EDGI</a> and <a href="https://screening-tools.com" class="gen-link">Public Environmental Data Partners</a>.
                Providing data from <a href="https://iris.fws.gov/APPS/ServCat/" class="gen-link">ServCat</a>.</p>
            </div>
        <div class="search-container">
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search catalog (exact match)...">
            </div>
            <button class="button" onclick="searchReferences()">Search</button>
            <button class="button clear-button" onclick="clearSearch()">Clear</button>
            <div id="searchSpinner" class="spinner"></div>
            <div id="resultCount"></div>
        </div>

        <div id="references-container">
"""

    # Add references to HTML
    for item in items:
        title = item.get("title", "No title")
        reference_type = item.get("referenceType", "Unknown type")
        reference_id = item.get("referenceId", "Unknown ID")
        abstract = item.get("abstract", "No abstract available")
        publication_date = item.get("publicationDate", "Unknown date")

        html_content += f"""
        <div class="reference" data-title="{title}" data-type="{reference_type}" data-abstract="{abstract}">
            <h2>{title}</h2>
            <div class="reference-details">
                <p><strong>Reference ID:</strong> {reference_id}</p>
                <p><strong>Type:</strong> {reference_type}</p>
                <p><strong>Publication Date:</strong> {publication_date}</p>
                <p><strong>Abstract:</strong> {abstract}</p>
            </div>
"""

        # Add linked resources
        if "linkedResources" in item and item["linkedResources"]:
            html_content += """
            <div class="resources">
                <h3>Linked Resources:</h3>
"""

            for resource in item["linkedResources"]:
                resource_name = resource.get("fileName", "Unknown file")
                resource_type = resource.get("resourceType", "Unknown type")
                resource_url = resource.get("url", "#").replace("http://", "https://")
                file_size = resource.get("fileSize", "Unknown size")
                if not file_size:
                    file_size = "Unknown size"
                if file_size != "Unknown size":
                    file_size = humanize_bytes(int(file_size))
                html_content += f"""
                <div class="resource">
                    <h3>{resource_name}</h3>
                    <p class="metadata"><strong>Type:</strong> {resource_type}</p>
                    <p class="metadata"><strong>Size:</strong> {file_size}</p>
                    <a href="{resource_url}" class="resource-link" target="_blank">View Resource</a>
                </div>
"""

            html_content += """
            </div>
"""

        html_content += """
        </div>
"""

    # Add footer and close HTML
    current_date = datetime.now().strftime("%Y-%m-%d")
    html_content += f"""
        </div>

        <div class="footer">
            <p>Generated on {current_date} | US Fish and Wildlife Services ServCat Data</p>
            <p>Created with ❤️ by Will Fitzgerald and EDGI</p>
        </div>
    </div>
</body>
</html>
"""

    # Write HTML to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML generated and saved to {output_file}")


if __name__ == "__main__":
    data_file = "output.json"
    output_file = "index.html"
    generate_html(data_file, output_file)
