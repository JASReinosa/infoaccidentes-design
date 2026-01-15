
import os
from bs4 import BeautifulSoup

ROOT_DIR = "."

# Mapping of old filename/fragment -> new canonical path relative to root
# We track by the "base" name usually found in hrefs
LINK_MAP = {
    "abogados.html": "abogados-trafico/index.html",
    "clinicas.html": "clinicas-accidentes-trafico/index.html",
    "calculadora.html": "calculadora-indemnizacion/index.html",
    "lesiones.html": "indemnizacion/index.html",
    "accidentes.html": "reclamar-accidente/index.html"
}

def get_relative_link(current_file_path, target_path_from_root):
    abs_current_dir = os.path.abspath(os.path.dirname(current_file_path))
    abs_root_dir = os.path.abspath(ROOT_DIR)
    
    rel_path_to_root = os.path.relpath(abs_root_dir, abs_current_dir)
    
    if rel_path_to_root == ".":
        return target_path_from_root
        
    final_path = os.path.join(rel_path_to_root, target_path_from_root)
    final_path = final_path.replace("\\", "/")
    
    return final_path

def standardize_links():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                process_file(file_path)
                count += 1
    print(f"Processed {count} files.")

def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        soup = BeautifulSoup(content, "html.parser")
        changed = False
        
        # We look for <a> tags where the href ends with one of our keys
        # OR exactly matches one of our keys (relative).
        # But easier: checking the HREF tells us intent.
        
        links = soup.find_all("a", href=True)
        for link in links:
            href = link['href']
            
            # Identify target based on old href
            target_key = None
            if "abogados.html" in href: target_key = "abogados.html"
            elif "clinicas.html" in href: target_key = "clinicas.html"
            elif "calculadora.html" in href: target_key = "calculadora.html"
            elif "lesiones.html" in href: target_key = "lesiones.html"
            elif "accidentes.html" in href: target_key = "accidentes.html"
            
            # If we found a match, check if we should update it
            if target_key:
                # Calculate what the NEW href should be
                new_canonical = LINK_MAP[target_key]
                correct_href = get_relative_link(file_path, new_canonical)
                
                # Only update if it's strictly the old style link or needs correction
                # We want to avoid replacing "reclamar-accidente/index.html" with "reclamar-accidente/index.html" repeatedly
                # But if the current href is "accidentes.html" or "../accidentes.html", we definitely replace.
                
                # Heuristic: if the current href doesn't contain the new folder name, it's definitely old.
                # Exception: if we are IN the folder, the link might be "index.html" or "#".
                
                # Check for old filenames
                if target_key in href: # e.g. ../abogados.html
                     if href != correct_href:
                         # Double check: if we already standardized it, href might be ../abogados-trafico/index.html
                         # But "abogados.html" is NOT in "abogados-trafico/index.html".
                         # So if "abogados.html" is in href, it's an OLD link.
                         link['href'] = correct_href
                         changed = True
            
        if changed:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print(f"Updated {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    standardize_links()
