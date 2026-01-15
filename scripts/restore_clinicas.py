
import csv
import os
import re
from bs4 import BeautifulSoup
import copy

# Constants
CSV_FILE = "NUEVO-contenido_migracion_limpio_v2-html nuevo de las urls viejas - Nuevas URLs y Contenido HTML.csv"
TEMPLATE_FILE = "clinicas_provincia.html"
OUTPUT_DIR = "clinicas-accidentes-trafico" # Target directory

def restore_clinicas():
    # 1. Load Template
    try:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            template_html = f.read()
    except FileNotFoundError:
        print(f"Error: Template {TEMPLATE_FILE} not found.")
        return

    # 2. Read CSV
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: CSV {CSV_FILE} not found.")
        return

    print(f"Found {len(rows)} rows in CSV.")

    processed_count = 0
    for row in rows:
        url = row["URL Nueva"].strip()
        content_html_raw = row["Contenido HTML"].strip()
        
        # Filter for clinicas pages only
        if "clinicas-accidentes-trafico" not in url:
            continue
            
        if not url or not content_html_raw:
            continue

        processed_count += 1
        
        # 3. Determine Output Path
        # URL likely: https://infoaccidentes.com/clinicas-accidentes-trafico/cantabria/
        path_suffix = url.replace("https://infoaccidentes.com/", "")
        if path_suffix.startswith("/"): path_suffix = path_suffix[1:]
        if path_suffix.endswith("/"): path_suffix += "index.html"
        elif not path_suffix.endswith(".html"): path_suffix += "/index.html"
        
        full_output_path = path_suffix
        
        # 4. Parse CSV Content
        source_soup = BeautifulSoup(content_html_raw, "html.parser")
        
        # Extract Title & Meta
        title_tag = source_soup.find("title")
        title_text = title_tag.get_text().strip() if title_tag else "Clínicas InfoAccidentes"
        
        meta_desc = source_soup.find("meta", attrs={"name": "description"})
        meta_desc_content = meta_desc["content"] if meta_desc else ""

        # Extract H1 for City Name logic
        h1_tag = source_soup.find("h1")
        h1_text = h1_tag.get_text().strip() if h1_tag else title_text

        # Determine City Name
        city_name = "Cantabria"
        
        # Priority: URL Slug (Cleaner)
        parts = path_suffix.split("/")
        if len(parts) >= 2 and parts[-2] != "clinicas-accidentes-trafico":
             city_slug = parts[-2]
             city_name = city_slug.replace("-", " ").title()
        else:
            # Fallback: Regex "en [City]"
            match = re.search(r"en\s+(.*?)$", h1_text, re.IGNORECASE)
            if match:
                 # Split by common separators to avoid capturing "Barcelona: Guia..."
                 candidate = match.group(1).split(":")[0].split("|")[0].strip()
                 if len(candidate) < 30: # Sanity check length
                     city_name = candidate

        # Extract Body Content to migrate
        source_body = source_soup.find("article")
        if not source_body:
             source_body = source_soup.find("body")
        
        migrated_nodes = []
        if source_body:
            for child in source_body.contents:
                if child.name == "h1": continue # Skip H1 as it stands in Hero
                migrated_nodes.append(child)

        # 5. Prepare New Page from Template
        template_soup = BeautifulSoup(template_html, "html.parser")
        
        # 5a. Update Title/Meta
        if template_soup.title: template_soup.title.string = title_text
        t_meta = template_soup.find("meta", attrs={"name": "description"})
        if t_meta: t_meta["content"] = meta_desc_content
        else:
            new_meta = template_soup.new_tag("meta", attrs={"name": "description", "content": meta_desc_content})
            template_soup.head.append(new_meta)
        
        # 5b. Localize Template (City Name & Attributes)
        target_replacements = {
            "Cantabria": city_name,
            "Santander": city_name,
            "Torrelavega": city_name,
            "Laredo": city_name,
            "Castro Urdiales": city_name,
            "Reinosa": city_name,
            "Peña Cabarga": "una zona complicada",
            "Picos de Europa": "la sierra"
        }
        
        def apply_replacements(text):
            if not text: return text
            for k, v in target_replacements.items():
                if k in text: text = text.replace(k, v)
            return text

        # Text Nodes
        for text_node in template_soup.find_all(string=True):
             if text_node.parent.name in ['script', 'style']: continue
             new_text = apply_replacements(text_node)
             if new_text != text_node: text_node.replace_with(new_text)

        # Attributes
        target_attrs = ['title', 'alt', 'placeholder', 'aria-label', 'content', 'data-alt']
        for tag in template_soup.find_all(True):
            for attr in target_attrs:
                if tag.has_attr(attr):
                    val = tag[attr]
                    if isinstance(val, str):
                        new_val = apply_replacements(val)
                        if new_val != val: tag[attr] = new_val

        # 5c. Update Hero H1
        t_h1 = template_soup.find("h1")
        if t_h1:
            # We can use the CSV H1 or construct one.
            # Using CSV H1 is safer for exact match to user intent.
            t_h1.string = h1_text
            # Optionally style the "en City" part if we want, but simple string is robust.

        # 5d. Fix Relative Paths
        def fix_path(path):
            if not path: return path
            if path.startswith(("http", "//", "#", "mailto:", "tel:")): return path
            if path.startswith("../"): return path
            return "../../" + path 

        for tag in template_soup.find_all(['a', 'link'], href=True):
            tag['href'] = fix_path(tag['href'])
        for tag in template_soup.find_all(['script', 'img'], src=True):
            tag['src'] = fix_path(tag['src'])

        # 5e. Inject CSV Content
        article = template_soup.find("article", class_="prose-content")
        if article:
            # Add divider
            divider = template_soup.new_tag("div", attrs={"class": "my-12 border-t border-slate-200"})
            article.append(divider)
            
            # Inject CSV content
            for node in migrated_nodes:
                article.append(copy.copy(node))
                
        # 6. Save
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
        with open(full_output_path, "w", encoding="utf-8") as out_f:
            out_f.write(str(template_soup.prettify()))
        
        print(f"Restored: {full_output_path}")

    print(f"Total Clinicas Pages Processed: {processed_count}")

if __name__ == "__main__":
    restore_clinicas()
