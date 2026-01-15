
import csv
import os
from bs4 import BeautifulSoup, Tag
import copy

CSV_FILE = "NUEVO-contenido_migracion_limpio_v2-html nuevo de las urls viejas - Nuevas URLs y Contenido HTML.csv"
TEMPLATE_FILE = "guia/accidente-sin-seguro/index.html"
OUTPUT_DIR = "."

def fix_path(path, depth):
    if not path: return path
    if path.startswith(("http", "//", "#", "mailto:", "tel:")): return path
    
    # Normalize path to root-relative by stripping existing "../"
    clean_path = path
    while clean_path.startswith("../"):
        clean_path = clean_path[3:]
        
    # Prepend correct depth
    if depth == 0:
        return clean_path
    
    prefix = "../" * depth
    return prefix + clean_path

def restore_generic():
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
        
        if not url: continue
        
        # Skip already processed categories
        if "clinicas-accidentes-trafico" in url: continue
        if "abogados-trafico" in url: continue
        
        # Also skip homepage if we don't want to overwrite index.html recklessly, 
        # BUT the user said "merged... updated".
        # If url is https://infoaccidentes.com/, let's process it?
        # index.html is in root.
        
        path_suffix = url.replace("https://infoaccidentes.com/", "")
        if path_suffix.startswith("/"): path_suffix = path_suffix[1:]
        
        if path_suffix == "":
            path_suffix = "index.html"
        elif path_suffix.endswith("/"): 
            path_suffix += "index.html"
        elif not path_suffix.endswith(".html"): 
            path_suffix += "/index.html"
            
        full_output_path = path_suffix
        
        # Determine depth for relative links
        # count slashes in path_suffix to know how deep we are
        # e.g. "index.html" -> 0
        # "guia/foo/index.html" -> 2
        depth = path_suffix.count("/")
        

    # 3. Parse Content
        if not content_html_raw:
            print(f"Skipping empty content for {url}")
            continue
            
        soup_content = BeautifulSoup(content_html_raw, "html.parser")
        
        # Extract Title & Meta
        title_tag = soup_content.find("title")
        title_text = title_tag.get_text().strip() if title_tag else "InfoAccidentes"
        
        meta_desc = soup_content.find("meta", attrs={"name": "description"})
        meta_desc_content = meta_desc["content"] if meta_desc else ""
        
        # Extract H1 from content to place in Hero
        h1_tag = soup_content.find("h1")
        h1_text = h1_tag.get_text().strip() if h1_tag else title_text
        if h1_tag: h1_tag.decompose() # Remove from body as it goes to hero
        
        # Extract Body Content
        # We prefer <article> content, but if not found, use body.
        source_body = soup_content.find("article")
        if not source_body:
             source_body = soup_content.find("body")

        if not source_body:
            # If still nothing, maybe the whole string is the body?
            # Create a tag wrapper
            body_html = soup_content.prettify()
        else:
            # Get inner HTML of body/article
            body_html = "".join([str(x) for x in source_body.contents])

        # 4. Load Template based on URL type
        current_template_file = TEMPLATE_FILE # Default
        target_template_files = ["/guia/", "/indemnizacion/", "/reclamar-accidente/"]
        use_new_style = any(x in url for x in target_template_files)

        if use_new_style:
            # Check if accidente-patinete.html exists, otherwise fallback
            if os.path.exists("accidente-patinete.html"):
                current_template_file = "accidente-patinete.html"
            
        try:
            with open(current_template_file, "r", encoding="utf-8") as f:
                template_html = f.read()
        except FileNotFoundError:
            print(f"Error: Template {current_template_file} not found. Skipping {url}")
            continue

        soup_template = BeautifulSoup(template_html, "html.parser")

        # 5. Inject Data into Template
        
        # Title
        if soup_template.title:
            soup_template.title.string = title_text
            
        # Meta description
        meta_tag = soup_template.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta_tag["content"] = meta_desc_content
        else:
            # Create if missing
            new_meta = soup_template.new_tag("meta", attrs={"name": "description", "content": meta_desc_content})
            if soup_template.head:
                soup_template.head.append(new_meta)

        if use_new_style:
            # --- NEW TEMPLATE INJECTION LOGIC ---
            
            # 1. Hero H1
            # Look for H1 in the hero section (usually defined by class or hierarchy)
            # In accidente-patinete.html, H1 is in <div class="max-w-4xl... text-center">...<h1>
            hero_h1 = soup_template.find("h1")
            if hero_h1:
                hero_h1.string = h1_text
                
            # 2. Intro Text (Optional - try to find first p)
            # The template has a <p class="text-lg ..."> below H1.
            # We might want to put the first paragraph of content there? 
            # For now, let's leave the content fully in the article to be safe, or just clear the hero description if we don't have one separate.
            # actually, let's find the p following the H1 in template and clear it or set it to generic?
            # Let's clean it up to avoid hardcoded "Patinete" text.
            if hero_h1:
                hero_p = hero_h1.find_next_sibling("p")
                if hero_p:
                    hero_p.decompose() # Remove specific intro text from template
            
            # 3. Main Article Content
            # Find <main id="articulo"> or <article class="prose">
            # new template has <main ... id="articulo"> ... <article class="prose ...">
            article_updated = False
            main_tag = soup_template.find("main", id="articulo")
            if main_tag:
                prose_article = main_tag.find("article", class_="prose")
                if prose_article:
                    prose_article.clear()
                    # Parse body_html back to tags to append
                    temp_soup = BeautifulSoup(body_html, "html.parser")
                    for child in (temp_soup.body.contents if temp_soup.body else temp_soup.contents): # Use body.contents if available, else root contents
                        prose_article.append(copy.copy(child))
                    article_updated = True
            
            # 4. TOC (Table of Contents)
            # The template has a hardcoded TOC. We should probably remove it because it won't match.
            if main_tag:
                toc_div = main_tag.find("div", class_="bg-slate-50")
                if toc_div:
                    # We could try to generate new TOC, but removing is safer to avoid mismatches
                    toc_div.decompose()

            # 5. Breadcrumbs
            # Modify the last <li> in breadcrumb to match valid page title
            nav_crumb = soup_template.find("nav", attrs={"aria-label": "Breadcrumb"})
            if nav_crumb:
                ol = nav_crumb.find("ol")
                if ol:
                    lis = ol.find_all("li")
                    if lis:
                        last_li = lis[-1]
                        # Clear existing content and add new text
                        last_li.clear()
                        last_li.append(title_text.split("-")[0].strip()) # Simple truncation

        else:
            # --- OLD GENERIC TEMPLATE LOGIC ---
            # H1
            h1_template = soup_template.find("h1")
            if h1_template:
                h1_template.string = h1_text
            
            # Content Container
            # Usually <div id="content"> or similar. 
            # In old `guia/accidente-sin-seguro/index.html`, it might be distinct.
            # Let's look for a generic container or main.
            content_div = soup_template.find("div", id="content") 
            if not content_div:
                content_div = soup_template.find("main")
            
            if content_div:
                content_div.clear()
                temp_soup = BeautifulSoup(body_html, "html.parser")
                for child in (temp_soup.body.contents if temp_soup.body else temp_soup.contents): # Use body.contents if available
                    content_div.append(copy.copy(child))

        # 6. Fix Relative Paths (CSS, JS, Images, Links)
        for tag in soup_template.find_all(["link", "script", "img", "a"]):
            if tag.name == "link" and tag.get("href"):
                tag["href"] = fix_path(tag["href"], depth)
            elif tag.name == "script" and tag.get("src"):
                tag["src"] = fix_path(tag["src"], depth)
            elif tag.name == "img" and tag.get("src"):
                tag["src"] = fix_path(tag["src"], depth)
            elif tag.name == "a" and tag.get("href"):
                tag["href"] = fix_path(tag["href"], depth)

        # 7. Write to File
        os.makedirs(os.path.dirname(full_output_path) if os.path.dirname(full_output_path) else ".", exist_ok=True)
        with open(full_output_path, "w", encoding="utf-8") as out_f:
            out_f.write(str(soup_template.prettify()))
            
        print(f"Restored: {full_output_path} (Template: {current_template_file})")
        processed_count += 1

    print(f"Total Generic Pages Processed: {processed_count}")

if __name__ == "__main__":
    restore_generic()
