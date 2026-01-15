
import os
from bs4 import BeautifulSoup

ROOT_DIR = "."

def check_navigation():
    missing_nav = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file == "index.html":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f, "html.parser")
                    
                    nav = soup.find("nav")
                    if not nav:
                        missing_nav.append(file_path)
                    else:
                        # Check if it has links
                        links = nav.find_all("a")
                        if len(links) < 3: # Arbitrary check for content
                            missing_nav.append(f"{file_path} (Nav found but empty/scant)")
                            
                except Exception as e:
                    print(f"Error checking {file_path}: {e}")

    if missing_nav:
        print("Pages missing navigation:")
        for p in missing_nav:
            print(f"- {p}")
    else:
        print("All index.html pages have navigation.")

if __name__ == "__main__":
    check_navigation()
