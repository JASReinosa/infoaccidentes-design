
import os
from bs4 import BeautifulSoup

ROOT_DIR = "."

def add_target_blank():
    count = 0
    updates = 0
    
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
                    
                    for a in soup.find_all("a", href=True):
                        href = a['href'].strip()
                        
                        # Check for outbound protocols
                        is_outbound = False
                        if href.lower().startswith(("http://", "https://", "mailto:", "tel:", "whatsapp:")):
                            is_outbound = True
                            
                        # Exception: internal absolute links if any (though usually we use relative)
                        # We assume http/https are external or intended to be treated as such (refresh)
                        
                        if is_outbound:
                            # Add target="_blank"
                            if a.get('target') != "_blank":
                                a['target'] = "_blank"
                                changed = True
                            
                            # Add rel="noopener noreferrer"
                            rel = a.get('rel', [])
                            if isinstance(rel, str):
                                rel = rel.split()
                            
                            if "noopener" not in rel:
                                rel.append("noopener")
                                changed = True
                            if "noreferrer" not in rel:
                                rel.append("noreferrer")
                                changed = True
                                
                            a['rel'] = rel
                            
                    if changed:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(soup.prettify())
                        updates += 1
                        # print(f"Updated {file_path}")
                        
                    count += 1
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"Scanned {count} files. Updated {updates} files.")

if __name__ == "__main__":
    add_target_blank()
