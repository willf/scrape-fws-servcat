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

    # Start building the HTML content with minimal whitespace
    html_parts = []
    html_parts.append(
        "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>US Fish and Wildlife Services ServCat References</title>"
    )

    # Include CSS directly in the HTML file
    html_parts.append("""<style>
body{font-family:Arial,sans-serif;line-height:1.6;margin:0;padding:20px;color:#333}
.container{max-width:1200px;margin:0 auto}
h1{color:#2c3e50;text-align:center;margin-bottom:10px}
.reference{margin-bottom:30px;padding:15px;border:1px solid #ddd;border-radius:5px;background-color:#f9f9f9}
.reference h2{margin-top:0;color:#3498db;border-bottom:1px solid #eee;padding-bottom:10px}
.reference-details{margin-bottom:15px}
.reference-details p{margin:5px 0}
.resources{margin-top:10px}
.resource{background-color:#fff;border:1px solid #eee;padding:10px;margin-bottom:10px;border-radius:3px}
.resource h3{margin-top:0;color:#2c3e50;font-size:16px}
.metadata{font-size:.9em;color:#666}
.resource-link{display:inline-block;margin-top:10px;background-color:#3498db;color:white;padding:5px 10px;text-decoration:none;border-radius:3px}
.resource-link:hover{background-color:#2980b9}
.gen-link{color:#3498db;text-decoration:none}
.gen-link:hover{text-decoration:underline}
.footer{text-align:center;margin-top:30px;font-size:.9em;color:#777}
.search-bar{margin-bottom:0;margin-right:10px;flex-grow:1;max-width:800px}
.search-bar input{width:100%;padding:8px;border:1px solid #ddd;border-radius:4px}
.made-by{width:100%;text-align:center;padding:10px 0}
.button{background-color:#3498db;color:white;padding:8px 15px;border:none;border-radius:4px;cursor:pointer;margin:0 5px}
.button:hover{background-color:#2980b9}
.clear-button{background-color:#e74c3c}
.clear-button:hover{background-color:#c0392b}
.search-container{display:flex;justify-content:center;align-items:center;margin-bottom:20px}
.spinner{display:none;width:20px;height:20px;border:3px solid rgba(0,0,0,.1);border-radius:50%;border-top-color:#3498db;animation:spin 1s ease-in-out infinite;margin-left:10px}
@keyframes spin{to{transform:rotate(360deg)}}
.page-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background-color:rgba(255,255,255,.7);display:flex;justify-content:center;align-items:center;z-index:1000}
.page-spinner{width:60px;height:60px;border:5px solid rgba(0,0,0,.1);border-radius:50%;border-top-color:#3498db;animation:spin 1s ease-in-out infinite}
#resultCount{margin-left:10px;font-style:italic}
</style>""")

    # Include minified JavaScript
    html_parts.append("""
<script>
function searchReferences(){document.getElementById('searchSpinner').style.display='block';setTimeout(()=>{const e=document.getElementById('searchInput').value.toLowerCase(),t=document.querySelectorAll('.reference');let n=0;for(const s of t){s.getAttribute('data-title').toLowerCase().includes(e)||s.getAttribute('data-type').toLowerCase().includes(e)||s.getAttribute('data-abstract').toLowerCase().includes(e)?(s.style.display='block',n++):s.style.display='none'}document.getElementById('searchSpinner').style.display='none',document.getElementById('resultCount').textContent=`${n} matches found`},50)}function clearSearch(){document.getElementById('searchInput').value='',document.getElementById('resultCount').textContent='';const e=document.querySelectorAll('.reference');for(const t of e)t.style.display='block'}function initSearchListener(){const e=document.getElementById('searchInput');e&&e.addEventListener('keypress',function(e){'Enter'===e.key&&searchReferences()})}window.onload=function(){initSearchListener(),setTimeout(()=>{document.getElementById('pageLoadOverlay').style.display='none'},500)};
</script>
</head><body><div id="pageLoadOverlay" class="page-overlay"><div class="page-spinner"></div></div><div class="container"><h1>US Fish and Wildlife Services ServCat Catalog</h1><div class="made-by"><p>Made with ❤️ by <a href="https://envirodatagov.org/" class="gen-link">EDGI</a> and <a href="https://screening-tools.com" class="gen-link">Public Environmental Data Partners</a>. Providing data from <a href="https://iris.fws.gov/APPS/ServCat/" class="gen-link">ServCat</a>.</p></div><div class="search-container"><div class="search-bar"><input type="text" id="searchInput" placeholder="Search catalog (exact match)..."></div><button class="button" onclick="searchReferences()">Search</button><button class="button clear-button" onclick="clearSearch()">Clear</button><div id="searchSpinner" class="spinner"></div><div id="resultCount"></div></div><div id="references-container">
""")

    # Process the data more efficiently
    reference_templates = []
    for item in items:
        title = item.get("title", "No title")
        reference_type = item.get("referenceType", "Unknown type")
        reference_id = str(item.get("referenceId", "Unknown ID"))
        abstract = item.get("abstract", "No abstract available")
        publication_date = item.get("publicationDate", "Unknown date")

        # Create reference HTML with minimal formatting
        reference_html = f'<div class="reference" data-title="{title}" data-type="{reference_type}" data-abstract="{abstract}"><h2>{title}</h2><div class="reference-details"><p><strong>Reference ID:</strong> {reference_id}</p><p><strong>Type:</strong> {reference_type}</p><p><strong>Publication Date:</strong> {publication_date}</p><p><strong>Abstract:</strong> {abstract}</p></div>'

        # Add linked resources
        if "linkedResources" in item and item["linkedResources"]:
            reference_html += '<div class="resources"><h3>Linked Resources:</h3>'

            for resource in item["linkedResources"]:
                resource_name = resource.get("fileName", "Unknown file")
                resource_type = resource.get("resourceType", "Unknown type")
                resource_url = resource.get("url", "#").replace("http://", "https://")
                file_size = resource.get("fileSize", "Unknown size")
                if not file_size:
                    file_size = "Unknown size"
                if file_size != "Unknown size":
                    file_size = humanize_bytes(int(file_size))

                reference_html += f'<div class="resource"><h3>{resource_name}</h3><p class="metadata"><strong>Type:</strong> {resource_type}</p><p class="metadata"><strong>Size:</strong> {file_size}</p><a href="{resource_url}" class="resource-link" target="_blank">View Resource</a></div>'

            reference_html += "</div>"

        reference_html += "</div>"
        reference_templates.append(reference_html)

    # Append all references at once
    html_parts.append("".join(reference_templates))

    # Add footer
    current_date = datetime.now().strftime("%Y-%m-%d")
    html_parts.append(
        f'</div><div class="footer"><p>Generated on {current_date} | US Fish and Wildlife Services ServCat Data</p><p>Created with ❤️ by Will Fitzgerald and EDGI</p></div></div></body></html>'
    )

    # Write HTML to file with minimal whitespace
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(html_parts))

    print(f"HTML generated and saved to {output_file}")


if __name__ == "__main__":
    data_file = "output.json"
    output_file = "index.html"
    generate_html(data_file, output_file)
