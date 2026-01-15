
import os
import re
from bs4 import BeautifulSoup
import copy

ROOT_DIR = "."
MASTER_FILE = "index.html"

def get_master_header():
    try:
        with open(MASTER_FILE, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            header = soup.find("header")
            if not header:
                raise Exception("No header found in master file")
            return header
    except Exception as e:
        print(f"Error reading master header: {e}")
        return None

def adjust_paths(soup_fragment, depth):
    if depth == 0:
        return soup_fragment
        
    prefix = "../" * depth
    
    # Adjust hrefs
    for tag in soup_fragment.find_all(attrs={"href": True}):
        href = tag['href']
        if not href.startswith(("http", "//", "#", "mailto:", "tel:")):
            tag['href'] = prefix + href
            
    # Adjust srcs
    for tag in soup_fragment.find_all(attrs={"src": True}):
        src = tag['src']
        if not src.startswith(("http", "//", "#", "data:")):
            tag['src'] = prefix + src
            
    return soup_fragment

def calculate_depth(file_path):
    # Relpath from root
    rel_path = os.path.relpath(os.path.dirname(file_path), ROOT_DIR)
    if rel_path == ".":
        return 0
    # Depth is number of separators + 1? No, relpath "guia" is depth 1. "guia/foo" is depth 2.
    # relpath "guia" -> depth 1.
    # relpath "." -> depth 0.
    return len(rel_path.split(os.sep))

def standardize_headers():
    master_header = get_master_header()
    if not master_header:
        return

    print("Master Header loaded.")
    count = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                # Skip the master file itself if we want, or just process it (depth 0, no change)
                if os.path.abspath(file_path) == os.path.abspath(MASTER_FILE):
                    continue
                    
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    soup = BeautifulSoup(content, "html.parser")
                    current_header = soup.find("header")
                    
                    if current_header:
                        # Prepare new header
                        depth = calculate_depth(file_path)
                        new_header = copy.copy(master_header)
                        new_header = adjust_paths(new_header, depth)
                        
                        # Replace
                        current_header.replace_with(new_header)
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(soup.prettify())
                        
                        count += 1
                        # print(f"Updated {file_path}")
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"Processed {count} files.")

if __name__ == "__main__":
    standardize_headers()
