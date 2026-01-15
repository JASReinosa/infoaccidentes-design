
import os
from bs4 import BeautifulSoup

ROOT_DIR = "."

# Mapping directory names to Display Titles
DIR_TITLES = {
    "reclamar-accidente": "Reclamar Accidente",
    "indemnizacion": "Indemnización",
    "clinicas-accidentes-trafico": "Clínicas",
    "abogados-trafico": "Abogados",
    "guia": "Guías",
    "lesiones": "Lesiones",
    "calculadora-indemnizacion": "Calculadora",
    # Subdirectories
    "coche": "Coche",
    "moto": "Moto",
    "atropello": "Atropello",
    "autobus": "Autobús",
    "camion": "Camión",
    "taxistas": "Taxistas",
    "ciclistas": "Ciclistas",
    "peaton": "Peatón",
    "patinete": "Patinete",
    "ocupante": "Ocupante",
    "latigazo-cervical": "Latigazo Cervical",
    "fracturas": "Fracturas",
    "traumatismos": "Traumatismos",
    "amputaciones": "Amputaciones",
    "quemaduras": "Quemaduras",
    "lesiones-medulares": "Lesiones Medulares",
    "cerebrales": "Daño Cerebral",
    "fallecimiento": "Fallecimiento",
    # Add more mappings as needed
}

def get_breadcrumb_html(file_path, soup):
    # Calculate depth and relative path to root
    # file_path is relative to ROOT_DIR, e.g. ./reclamar-accidente/coche/index.html
    
    parts = os.path.normpath(file_path).split(os.sep)
    # Filter out empty or '.'
    parts = [p for p in parts if p and p != '.']
    
    if not parts:
        return None
        
    filename = parts[-1]
    dirs = parts[:-1]
    
    # Calculate relation to root for links
    # If file is in ., depth is 0. link to root is ./
    # If file is in ./dir, depth is 1. link to root is ../
    depth = len(dirs)
    to_root = "../" * depth if depth > 0 else "./"
    
    # Build items list: (Title, Link)
    items = []
    
    # 1. Home
    items.append(("Inicio", f"{to_root}index.html"))
    
    # 2. Directories
    current_rel_path = to_root
    for i, d in enumerate(dirs):
        title = DIR_TITLES.get(d, d.replace("-", " ").title())
        # Link to index.html of that directory
        # For the link, we need to go down from root? No, relative from current file.
        # It's cleaner to build absolute path from project root and then convert to relative?
        # Or just build relative step by step.
        
        # Actually easier:
        # If we are at depth N, root is N steps back.
        # Dir i is (N - i) steps back? No.
        # Let's say we are in /a/b/c/index.html
        # Home: ../../../index.html
        # a: ../../index.html
        # b: ../index.html
        # c: ./index.html (Current)
        
        # Wait, if we are in /a/b/c/index.html, "c" is the directory we are IN, so it's the current page usually?
        # Typically breadcrumb is: Home > A > B > C (Current Page)
        
        # Let's calculate the relative link to the directory's index
        # steps_back = depth - (i + 1)
        # link = "../" * steps_back + "index.html"
        
        steps_back = len(dirs) - (i + 1)
        if steps_back > 0:
            link = "../" * steps_back + "index.html"
        else:
            link = "index.html" # Link to itself if it's the index
            
        items.append((title, link))
        
    # 3. Current Page
    # If filename is index.html, the last directory IS the current page title usually.
    # But sometimes we want the page title explicitly.
    # Standard practice: Home > Section > SubSection (Current)
    # If we are in /reclamar-accidente/index.html
    # Breadcrumb: Home > Reclamar Accidente
    # The last item "Reclamar Accidente" is text only (active).
    
    # If we are in /accidente-patinete.html (Root file)
    # Breadcrumb: Home > Accidente Patinete
    
    # Logic:
    # If filename is index.html, the last dir is the current item.
    # If filename is not index.html, the file itself is the current item.
    
    if filename == "index.html":
        if items:
            # The last item added from dirs is actually the current page
            # Make it text only (remove link)
            last_title, last_link = items.pop()
            items.append((last_title, None))
        else:
            # Root index.html
            items = [("Inicio", None)]
    else:
        # File is a page inside the last dir
        # e.g. /reclamar-accidente/contact.html -> Home > Reclamar Accidente > Contact
        # Check title
        page_title = filename.replace(".html", "").replace("-", " ").title()
        
        # Try to get h1 for better title
        h1 = soup.find("h1")
        if h1:
            # Too long usually. Use Mapping or filename.
            # Special case for known files
            if filename == "accidente-patinete.html":
                page_title = "Patinete Eléctrico"
        
        items.append((page_title, None))
        
    # Build HTML
    # <nav aria-label="Breadcrumb" class="flex text-sm text-gray-500">
    #  <ol class="flex items-center space-x-2"> ... </ol>
    # </nav>
    
    nav = soup.new_tag("nav", attrs={"aria-label": "Breadcrumb", "class": "flex text-sm text-gray-500"})
    ol = soup.new_tag("ol", attrs={"class": "flex items-center space-x-2"})
    nav.append(ol)
    
    separator = soup.new_tag("span", attrs={"class": "text-gray-300"})
    separator.string = "/"
    
    for i, (title, link) in enumerate(items):
        li = soup.new_tag("li")
        
        if link:
            a = soup.new_tag("a", href=link, attrs={"class": "hover:text-primary transition-colors"})
            a.string = title
            li.append(a)
        else:
            # Current item
            li['class'] = "font-medium text-gray-900"
            li.string = title
            
        ol.append(li)
        
        # Add separator if not last
        if i < len(items) - 1:
            li_sep = soup.new_tag("li")
            li_sep.append(separator.__copy__())
            ol.append(li_sep)
            
    return nav

def update_breadcrumbs():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f.read(), "html.parser")
                    
                    # Find existing breadcrumb
                    # Usually <nav aria-label="Breadcrumb">
                    old_nav = soup.find("nav", attrs={"aria-label": "Breadcrumb"})
                    
                    if old_nav:
                        new_nav = get_breadcrumb_html(file_path, soup)
                        if new_nav:
                            old_nav.replace_with(new_nav)
                            
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(soup.prettify())
                            count += 1
                            # print(f"Updated {file}")
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    print(f"Updated breadcrumbs in {count} files.")

if __name__ == "__main__":
    update_breadcrumbs()
