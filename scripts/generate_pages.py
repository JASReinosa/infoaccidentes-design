
import csv
import os
from bs4 import BeautifulSoup
import re

CSV_FILE = "NUEVO-contenido_migracion_limpio_v2-html nuevo de las urls viejas - Nuevas URLs y Contenido HTML.csv"
TEMPLATE_FILE = "index.html"
OUTPUT_DIR = "."

def generate_pages():
    # 1. Load the Template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_html = f.read()

    # 2. Read the CSV
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            url = row["URL Nueva"].strip()
            content_html_raw = row["Contenido HTML"].strip()
            
            if not url or not content_html_raw:
                print(f"Skipping empty row: {url}")
                continue

            # 3. Determine Output Path
            # Remove protocol and domain
            path = url.replace("https://infoaccidentes.com/", "")
            if path.startswith("/"):
                path = path[1:]
            
            # If path is empty, it's the home page, skip it or handle specifically? 
            # User said "add pages", assuming new pages. Index already exists.
            if not path:
                print(f"Skipping homepage URL: {url}")
                continue
                
            # If path ends with /, append index.html
            if path.endswith("/"):
                path += "index.html"
            elif not path.endswith(".html"):
                # If it doesn't end in /, map it to a directory/index.html anyway for clean URLs?
                # Or just append .html? 
                # The user's URLs end in slash (e.g. /contacto/), so they imply folders.
                path += "/index.html"

            full_output_path = os.path.join(OUTPUT_DIR, path)
            os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
            
            # 4. Parse the Content HTML
            soup_content = BeautifulSoup(content_html_raw, "html.parser")
            
            # Extract Title
            title_tag = soup_content.find("title")
            title_text = title_tag.get_text() if title_tag else "InfoAccidentes"
            
            # Extract Meta Description
            meta_desc_tag = soup_content.find("meta", attrs={"name": "description"})
            meta_desc_content = meta_desc_tag["content"] if meta_desc_tag else ""
            
            # Extract Body Content
            # Prefer <article> if exists, otherwise <body>
            body_content_tag = soup_content.find("article")
            if not body_content_tag:
                 body_content_tag = soup_content.find("body")
            
            if not body_content_tag:
                print(f"No body/article found for {url}, skipping.")
                continue

            # 5. Prepare the Page
            soup_template = BeautifulSoup(template_html, "html.parser")
            
            # Update Title
            if soup_template.title:
                soup_template.title.string = title_text
            else:
                new_title = soup_template.new_tag("title")
                new_title.string = title_text
                soup_template.head.append(new_title)
                
            # Update Meta Description
            template_meta_desc = soup_template.find("meta", attrs={"name": "description"})
            if template_meta_desc:
                template_meta_desc["content"] = meta_desc_content
            else:
                new_meta = soup_template.new_tag("meta", attrs={"name": "description", "content": meta_desc_content})
                soup_template.head.append(new_meta)

            # Clear Main and Inject Content
            main_tag = soup_template.find("main")
            if main_tag:
                main_tag.clear()
                # Wrap content in a container for consistent spacing
                container = soup_template.new_tag("div", attrs={"class": "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 prose prose-lg"})
                # We need to append the children of body_content_tag to the container
                # copy children to avoid issues
                for child in list(body_content_tag.contents):
                    container.append(child)
                main_tag.append(container)
            else:
                print(f"Error: No <main> tag found in template.")
                break
                
            # 6. Save File
            with open(full_output_path, "w", encoding="utf-8") as out_f:
                out_f.write(str(soup_template.prettify()))
            
            print(f"Generated: {full_output_path}")

if __name__ == "__main__":
    generate_pages()
