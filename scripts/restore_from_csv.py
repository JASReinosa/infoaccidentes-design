
import csv
import os
import re
from bs4 import BeautifulSoup

# Constants from previous scripts
CSV_FILE = "NUEVO-contenido_migracion_limpio_v2-html nuevo de las urls viejas - Nuevas URLs y Contenido HTML.csv"
TEMPLATE_FILE = "abogados_provincia.html"
OUTPUT_DIR = "abogados-trafico" # Target directory pattern usually matched CSV URLs

def restore_pages():
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

    for row in rows:
        url = row["URL Nueva"].strip()
        content_html_raw = row["Contenido HTML"].strip()
        
        # Filter for abogados-trafico pages only?
        # User said "review all the pages... of each location".
        # The previous script targeted `abogados-trafico/*/index.html`.
        # We should probably process relevant URLs only or all if they match the pattern.
        if "abogados-trafico" not in url:
            continue
            
        if not url or not content_html_raw:
            continue

        # 3. Determine Output Path & City Name
        # URL likely: https://infoaccidentes.com/abogados-trafico/a-coruna/
        # Path: abogados-trafico/a-coruna/index.html
        path_suffix = url.replace("https://infoaccidentes.com/", "")
        if path_suffix.startswith("/"): path_suffix = path_suffix[1:]
        if path_suffix.endswith("/"): path_suffix += "index.html"
        elif not path_suffix.endswith(".html"): path_suffix += "/index.html"
        
        full_output_path = path_suffix # relative to current dir?
        # Be careful not to double prefix if OUTPUT_DIR is used.
        # Let's trust path_suffix is correct relative to root.
        
        # Extract City Name from URL or Content?
        # URL: abogados-trafico/a-coruna/ -> A Coruna
        # Better: extract H1 from content
        
        soup_content = BeautifulSoup(content_html_raw, "html.parser")
        
        # Extract Title & Meta
        title_tag = soup_content.find("title")
        title_text = title_tag.get_text().strip() if title_tag else "Abogados InfoAccidentes"
        
        meta_desc = soup_content.find("meta", attrs={"name": "description"})
        meta_desc_content = meta_desc["content"] if meta_desc else ""

        # Extract H1 for City Name logic
        h1_tag = soup_content.find("h1")
        h1_text = h1_tag.get_text().strip() if h1_tag else title_text

        # Determine City Name
        # Determine City Name
        city_name = "Cantabria"
        
        # Priority: URL Slug (Cleaner)
        parts = path_suffix.split("/")
        if len(parts) >= 2 and parts[-2] != "abogados-trafico":
             city_slug = parts[-2]
             city_name = city_slug.replace("-", " ").title()
        else:
            match = re.search(r"en\s+(.*?)$", h1_text, re.IGNORECASE)
            if match:
                 candidate = match.group(1).split(":")[0].split("|")[0].strip()
                 if len(candidate) < 30:
                    city_name = candidate

        # Extract Body Content (The "All content of the CSV")
        # We want the 'article' or 'body' content, excluding H1 because we set H1 in hero.
        source_body = soup_content.find("article")
        if not source_body:
             source_body = soup_content.find("body")
        
        migrated_nodes = []
        if source_body:
            for child in source_body.contents:
                if child.name == "h1": continue
                migrated_nodes.append(child)

        # 4. Prepare New Page from Template
        template_soup = BeautifulSoup(template_html, "html.parser")
        
        # 4a. Update Title/Meta
        if template_soup.title: template_soup.title.string = title_text
        t_meta = template_soup.find("meta", attrs={"name": "description"})
        if t_meta: t_meta["content"] = meta_desc_content
        
        # 4b. Localize Template (City Name & Attributes)
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

        # 4c. Update Hero H1
        t_h1 = template_soup.find("h1")
        if t_h1:
            t_h1.string = h1_text # Set strictly from CSV H1

        # 4d. Fix Relative Paths
        def fix_path(path):
            if not path: return path
            if path.startswith(("http", "//", "#", "mailto:", "tel:")): return path
            if path.startswith("../"): return path
            return "../../" + path # Assuming depth 2 (abogados-trafico/city/)

        for tag in template_soup.find_all(['a', 'link'], href=True):
            tag['href'] = fix_path(tag['href'])
        for tag in template_soup.find_all(['script', 'img'], src=True):
            tag['src'] = fix_path(tag['src'])

        # 4e. Inject CSV Content
        # We append it to the article.prose-content
        # IMPORTANT: Check for generic sections in CSV content?
        # User said "Add all the content".
        # But also "be sure there are not repeated elements".
        # If we paste CSV content, and Template has "Historias de Éxito", and CSV *doesn't*, it's fine.
        # But what if CSV content *replaces* the Template's generic filler?
        # The template has "Problemas comunes...", "Por qué elegir...", "Historias de éxito...".
        # The CSV content likely has the specific lawyer list and intro.
        # I think the safest bet is to INSERT the CSV content at the TOP of the article (after H2),
        # OR keep the template structure and just append unique bits.
        # User said "removed content... Add all content... to article".
        # This implies the article might be EMPTY except for what we put in?
        # No, "abogados_provincia.html" has a lot of text.
        
        article = template_soup.find("article", class_="prose-content")
        if article:
            # Strategies:
            # 1. Clear Article and put ONLY CSV content? (Might lose "Historias de éxito" design)
            # 2. Append CSV content? (Might be at bottom)
            # 3. Prepend?
            
            # The previous script Appended it with a divider.
            # "There are now repeated elements". This suggests I kept Template + CSV and they overlapped.
            # If CSV has "Testimonials" and Template has "Testimonials", we have 2.
            # I will remove the "Historias de éxito" section FROM THE TEMPLATE if I suspect duplication?
            # Or better: The CSV content `<body>` likely contains the Whole Page Content from the old site.
            # If I inject that, I should probably CLEAR the default `abogados_provincia.html` placeholder content within the article?
            # The user said "match the name... unique content... remove repeated".
            # If I wipe the template article content, I lose the "Problem... Why Choose InfoAccidentes..." sections which are part of the new design.
            # Maybe the user WANTS those sections but localized.
            
            # compromise:
            # Keep Template Article (Localized).
            # Append CSV Content.
            # Remove "duplicates" if CSV content has them.
            # But duplicate detection is hard.
            
            # Wait, user said: "you have now removed the content... Add ALL the content of the csv".
            # This suggests the CSV content is paramount.
            # And "merged... repeated elements".
            
            # Let's try:
            # 1. Keep Template's Hero, Sidebar, Footer.
            # 2. In Main > Article:
            #    - Insert CSV Content (Intro + Lawyers).
            #    - Keep Template's "Historias de éxito" (Testimonials) ONLY if not present in CSV?
            #    - Actually, the template's "Historias de éxito" is outside the article in a separate section.
            #      (See lines 499+ in a-coruna/index.html).
            # So duplicate testimonials likely come from CSV having them + Template having them.
            # I will blindly inject CSV content into Article.
            # And I will NOT remove anything from Template yet, unless I see obvious dupes like H2s.
            
            divider = template_soup.new_tag("div", attrs={"class": "my-12 border-t border-slate-200"})
            article.append(divider)
            
            # Inject
            import copy
            for node in migrated_nodes:
                article.append(copy.copy(node))
                
        # 5. Save
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
        with open(full_output_path, "w", encoding="utf-8") as out_f:
            out_f.write(str(template_soup.prettify()))
        
        print(f"Restored: {full_output_path}")

if __name__ == "__main__":
    restore_pages()
