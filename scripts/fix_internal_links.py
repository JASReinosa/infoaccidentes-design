import os
import re
from bs4 import BeautifulSoup

ROOT_DIR = "."

def fix_internal_links():
    print("Iniciando escaneo para corregir enlaces internos...")
    count = 0
    
    # Walk through directory
    for root, dirs, files in os.walk(ROOT_DIR):
        # Exclude system folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    soup = BeautifulSoup(content, "html.parser")
                    changed = False
                    
                    # Find all <a> tags with href
                    links = soup.find_all("a", href=True)
                    for link in links:
                        href = link['href']
                        
                        # 1. Check if it's an absolute link to our own domain
                        # e.g., https://infoaccidentes.com/contacto/ -> /contacto/
                        is_absolute_internal = href.startswith(("https://infoaccidentes.com", "http://infoaccidentes.com", "https://www.infoaccidentes.com", "http://www.infoaccidentes.com"))
                        
                        if is_absolute_internal:
                            # Convert to relative path from root
                            # Remove domain part
                            path_part = re.sub(r'https?://(www\.)?infoaccidentes\.com', '', href)
                            if not path_part.startswith("/"):
                                path_part = "/" + path_part
                            
                            # Let's calculate depth of the current file
                            rel_dir = os.path.relpath(os.path.dirname(file_path), ROOT_DIR)
                            if rel_dir == ".":
                                depth = 0
                            else:
                                depth = len(rel_dir.split(os.sep))
                            
                            prefix = "../" * depth
                            if path_part == "/":
                                new_href = prefix + "index.html" if depth > 0 else "index.html"
                            else:
                                # if it starts with /, replace with prefix
                                new_href = prefix + path_part[1:]
                                
                            link['href'] = new_href
                            href = new_href # update for subsequent checks
                            changed = True
                            
                        # 2. Check for internal link targeting new tabs or containing noreferrer
                        # An internal link is anything that doesn't start with http/https/mailto/tel/etc.
                        is_external = href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:"))
                        
                        if not is_external:
                            # Check target
                            if link.has_attr('target') and link['target'] == '_blank':
                                del link['target']
                                changed = True
                            
                            # Check rel
                            if link.has_attr('rel'):
                                rel_values = link['rel']
                                # Remove noopener and noreferrer if present
                                new_rel = [r for r in rel_values if r not in ['noopener', 'noreferrer']]
                                if not new_rel:
                                    del link['rel']
                                else:
                                    link['rel'] = new_rel
                                changed = True
                                
                    if changed:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(soup.prettify())
                        count += 1
                        # print(f"Corregidos enlaces en: {file_path}")
                        
                except Exception as e:
                    print(f"Error procesando {file_path}: {e}")

    print(f"Finalizado. Total archivos HTML con enlaces internos corregidos: {count}")

if __name__ == "__main__":
    fix_internal_links()
