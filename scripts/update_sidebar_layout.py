
import os
from bs4 import BeautifulSoup
import re

ROOT_DIR = "."

def calculate_depth(file_path):
    rel_path = os.path.relpath(os.path.dirname(file_path), ROOT_DIR)
    if rel_path == ".": return 0
    return len(rel_path.split(os.sep))

def update_layout():
    count = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    soup = BeautifulSoup(content, "html.parser")
                    changed = False
                    
                    # 1. Remove "Other Articles" block and replace with container
                    # Search text "Otros artículos de interés"
                    # But better, find the container. 
                    
                    # Pattern: <div class="bg-slate-50 p-6 rounded-xl border border-slate-200"> ... <h3>Otros artículos...
                    
                    target_div = None
                    for div in soup.find_all("div"):
                        h3 = div.find("h3")
                        if h3 and "Otros artículos de interés" in h3.get_text():
                            target_div = div
                            break
                    
                    if target_div:
                        # We found the block. Rebuild it.
                        # We want to keep the wrapper styling but empty content
                        # Or just replace contents.
                        
                        target_div.clear()
                        target_div['id'] = "related-articles-container"
                        # Ensure class "relative" for the link hacks
                        if "relative" not in target_div.get("class", []):
                             target_div['class'] = target_div.get("class", []) + ["relative"]
                             
                        changed = True
                        
                    # 2. Fix Sticky Overlap
                    # Find div with "sticky top-24" inside aside?
                    # "bg-white p-6 rounded-xl shadow-lg border border-gray-100 sticky top-24"
                    
                    sticky_cards = soup.find_all("div", class_=lambda x: x and "sticky" in x and "top-24" in x)
                    for card in sticky_cards:
                        # Check if it is the "Por qué elegir" card
                        if card.find(string=re.compile("Por qué elegir InfoAccidentes")):
                            # Remove sticky and top-24
                            classes = card['class']
                            if "sticky" in classes: classes.remove("sticky")
                            if "top-24" in classes: classes.remove("top-24")
                            card['class'] = classes
                            changed = True

                    # 3. Inject Script
                    if changed:
                        depth = calculate_depth(file_path)
                        prefix = "../" * depth
                        script_src = f"{prefix}js/related-articles.js"
                        
                        # check if already exists
                        if not soup.find("script", src=script_src):
                            new_script = soup.new_tag("script", src=script_src)
                            soup.body.append(new_script)
                            
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(soup.prettify())
                        count += 1
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"Updated {count} files with new sidebar layout.")

if __name__ == "__main__":
    update_layout()
