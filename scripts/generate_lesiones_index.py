
import os
from bs4 import BeautifulSoup
import copy

SOURCE_FILE = "lesiones.html"
TARGET_DIR = "indemnizacion"
TARGET_FILE = os.path.join(TARGET_DIR, "index.html")

# Icon mapping for specific slugs
ICON_MAP = {
    "latigazo-cervical": "medical_services",
    "traumatismo-craneoencefalico": "psychology",
    "fallecimiento": "heart_broken",
    "lesion-medular": "accessible",
    "amputacion": "accessible_forward", # specialized
    "cervicalgia": "medical_services",
    "cicatrices": "dermatology",
    "dorsalgia": "back_hand", # closest approximation or generic
    "esguince-tobillo": "foot_bones", # doesn't exist, maybe do generic
    "fractura-clavicula": "orthopedics", # generic bone
    "fractura-femur": "orthopedics",
    "fractura-muneca": "hands", # custom?
    "fractura-perone": "orthopedics",
    "fractura-tibia": "orthopedics",
    "hernia-discal": "monitor_heart", # maybe?
    "lumbalgia": "accessibility_new",
    "paraplejia": "accessible",
    "tetraplejia": "accessible",
    "perdida-audicion": "hearing",
    "perdida-vision": "visibility",
    "perjuicio-estetico": "face",
    "estres-postraumatico": "psychology",
}

DEFAULT_ICON = "healing"

def fix_path_depth(path):
    if not path: return path
    if path.startswith(("http", "//", "#", "mailto:", "tel:")): return path
    if path.startswith("#"): return path
    # Moving from root to /indemnizacion/ (depth 1)
    return "../" + path

def get_page_details(file_path):
    """Extracts title and description from an HTML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            
        # Meta description for the card text
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc else "Guía completa sobre esta lesión y su indemnización."
        
        # Optimize description length for card
        # Take first sentence or truncate
        if len(description) > 120:
             description = description[:117] + "..."

        return description
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return "Guía completa con información legal y médica."

def generate_lesiones_index():
    print(f"Reading {SOURCE_FILE}...")
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: {SOURCE_FILE} not found.")
        return

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Update relative paths for depth change (Root -> /indemnizacion/)
    print("Fixing relative paths...")
    for tag in soup.find_all(['link', 'script', 'img', 'a']):
        if tag.name == 'link' and tag.get('href'):
            tag['href'] = fix_path_depth(tag['href'])
        elif tag.name == 'script' and tag.get('src'):
            tag['src'] = fix_path_depth(tag['src'])
        elif tag.name == 'img' and tag.get('src'):
            tag['src'] = fix_path_depth(tag['src'])
        elif tag.name == 'a' and tag.get('href'):
            original_href = tag.get('href')
            if original_href == "lesiones.html":
                tag['href'] = "index.html" # Self reference
            else:
                tag['href'] = fix_path_depth(original_href)

    # 2. Gather content from subdirectories
    print(f"Scanning {TARGET_DIR} for injuries...")
    injuries = []
    if os.path.exists(TARGET_DIR):
        for entry in os.scandir(TARGET_DIR):
            if entry.is_dir():
                index_path = os.path.join(entry.path, "index.html")
                if os.path.exists(index_path):
                    slug = entry.name
                    title = slug.replace("-", " ").title()
                    # Fix special cases like "De" -> "de" if we want, or just keep title case
                    
                    description = get_page_details(index_path)
                    icon = ICON_MAP.get(slug, DEFAULT_ICON)
                    
                    injuries.append({
                        "slug": slug,
                        "title": title,
                        "description": description,
                        "icon": icon
                    })
    
    # Sort alphabetically
    injuries.sort(key=lambda x: x["title"])
    print(f"Found {len(injuries)} injury types.")

    # 3. Build new grid HTML
    grid_html = ""
    for injury in injuries:
        link = f"{injury['slug']}/"
        grid_html += f"""
        <a class="group bg-white p-8 rounded-xl shadow-sm hover:shadow-md border border-slate-100 hover:border-primary/30 transition-all flex flex-col items-center text-center"
            href="{link}">
            <div class="bg-primary/10 p-4 rounded-full mb-4 group-hover:bg-primary/20 transition-colors">
                <span class="material-symbols-outlined text-primary text-4xl">{injury['icon']}</span>
            </div>
            <h3 class="text-lg font-bold text-text-dark mb-2">{injury['title']}</h3>
            <p class="text-sm text-text-muted">{injury['description']}</p>
        </a>
        """

    # 4. Inject grid into the template
    # The grid is inside a section. We need to find the container of the existing grid.
    # Existing grid has class "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    print("Replacing grid content...")
    grid_container = soup.find("div", class_="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6")
    if grid_container:
        # Clear existing children
        grid_container.clear()
        # Append new children
        grid_container.append(BeautifulSoup(grid_html, "html.parser"))
    else:
        print("Error: Could not find grid container.")

    # 5. Save
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
        
    print(f"Successfully generated {TARGET_FILE}")

if __name__ == "__main__":
    generate_lesiones_index()
