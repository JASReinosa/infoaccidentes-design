
import os
from bs4 import BeautifulSoup

ROOT_DIR = "."
TARGET_PATH_FROM_ROOT = "guia/index.html"

def get_relative_link(current_file_path):
    # Calculate depth
    # e.g. ./index.html -> depth 0
    # ./guia/index.html -> depth 1
    # ./reclamar-accidente/coche/index.html -> depth 2
    
    abs_current_dir = os.path.abspath(os.path.dirname(current_file_path))
    abs_root_dir = os.path.abspath(ROOT_DIR)
    
    # Calculate relative path from current dir to root
    rel_path_to_root = os.path.relpath(abs_root_dir, abs_current_dir)
    
    # Combine with target path from root
    if rel_path_to_root == ".":
        return TARGET_PATH_FROM_ROOT
        
    final_path = os.path.join(rel_path_to_root, TARGET_PATH_FROM_ROOT)
    # Normalize (handle windows/unix separators if needed, though usually / for web)
    final_path = final_path.replace("\\", "/")
    
    # Special case: if we are inside /guia/, the link to guia/index.html is just index.html
    # But relpath logic handles it: ../guia/index.html. Does it?
    # inside guia: rel to root is ..
    # path is ../guia/index.html. This is correct.
    # But if we are in guia/index.html itself, referencing itself is fine.
    
    return final_path

def update_navigation():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        # Exclude hidden dirs or specific dirs to be safe
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
        
        target_href = get_relative_link(file_path)
        
        # 1. Desktop Nav
        # Selector: nav class="hidden md:flex space-x-8"
        desktop_nav = soup.find("nav", class_="hidden md:flex space-x-8")
        if desktop_nav:
            # Check if link exists
            exists = False
            for a in desktop_nav.find_all("a"):
                if "Guías" in a.get_text():
                    # Update href just in case
                    if a['href'] != target_href:
                        a['href'] = target_href
                        changed = True
                    exists = True
                    break
            
            if not exists:
                new_link = soup.new_tag("a", href=target_href)
                new_link['class'] = "text-text-muted hover:text-primary font-medium transition-colors"
                new_link.string = "Guías"
                desktop_nav.append(new_link)
                changed = True

        # 2. Mobile Nav
        # Selector: div id="mobile-menu" -> div class="px-4..."
        mobile_menu = soup.find("div", id="mobile-menu")
        if mobile_menu:
            container = mobile_menu.find("div", class_="px-4")
            if container:
                # Find where to insert (before the button container which has border-t)
                button_container = container.find("div", class_="border-t")
                
                # Check for existing
                exists = False
                for a in container.find_all("a", recursive=False):
                    if "Guías" in a.get_text():
                        if a['href'] != target_href:
                            a['href'] = target_href
                            changed = True
                        exists = True
                        break
                
                if not exists:
                    new_link = soup.new_tag("a", href=target_href)
                    new_link['class'] = "block py-3 px-4 text-base font-medium text-text-dark hover:bg-gray-50 rounded-md"
                    new_link.string = "Guías"
                    
                    if button_container:
                        button_container.insert_before(new_link)
                    else:
                        container.append(new_link)
                    changed = True

        # 3. Footer Link
        # Text "Guías de Reclamación"
        # Since text might vary slightly or be nested, search all 'a' tags
        for a in soup.find_all("a"):
            if a.string and "Guías de Reclamación" in a.string:
                if a['href'] != target_href:
                    a['href'] = target_href
                    changed = True

        if changed:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print(f"Updated {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    update_navigation()
