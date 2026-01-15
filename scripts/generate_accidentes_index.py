
import os
from bs4 import BeautifulSoup
import copy

SOURCE_FILE = "accidentes.html"
TARGET_DIR = "reclamar-accidente"
TARGET_FILE = os.path.join(TARGET_DIR, "index.html")

# Icon mapping for slugs
ICON_MAP = {
    # Existing in accidents.html
    "coche": "directions_car",
    "moto": "two_wheeler",
    "atropello": "directions_walk",
    "bicicleta": "pedal_bike",
    "patinete-electrico": "electric_scooter",
    "transporte-publico": "directions_bus",
    "pasajero": "airline_seat_recline_normal",
    "rotonda": "u_turn_right",
    "alcance-trasero": "minor_crash",
    "in-itinere": "work",
    "taxi": "local_taxi",
    "animales-cinegeticos": "pets",
    
    # New additions requiring icons
    "alcance-cadena": "minor_crash",
    "autobus": "directions_bus",
    "camion": "local_shipping",
    "ciclistas": "pedal_bike",
    "ciclomotor": "moped",
    "coche-de-alquiler": "car_rental",
    "furgoneta": "airport_shuttle",
    "peaton": "directions_walk",
    "vtc": "local_taxi",
}

DEFAULT_ICON = "traffic"

def fix_path_depth(path):
    if not path: return path
    if path.startswith(("http", "//", "#", "mailto:", "tel:")): return path
    if path.startswith("#"): return path
    # Moving from root to /reclamar-accidente/ (depth 1)
    return "../" + path

def get_page_details(file_path):
    """Extracts title and description from an HTML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            
        # Meta description for the card text
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc else "Guía completa para reclamar su indemnización."
        
        # Optimize description length for card
        if len(description) > 120:
             description = description[:117] + "..."

        return description
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return "Guía completa con información legal."

def generate_accidentes_index():
    print(f"Reading {SOURCE_FILE}...")
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: {SOURCE_FILE} not found.")
        return

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Update relative paths for depth change (Root -> /reclamar-accidente/)
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
            if original_href == "accidentes.html":
                tag['href'] = "index.html" # Self reference
            else:
                tag['href'] = fix_path_depth(original_href)

    # 2. Gather content from subdirectories
    print(f"Scanning {TARGET_DIR} for accident types...")
    accidents = []
    if os.path.exists(TARGET_DIR):
        for entry in os.scandir(TARGET_DIR):
            if entry.is_dir():
                index_path = os.path.join(entry.path, "index.html")
                if os.path.exists(index_path):
                    slug = entry.name
                    title = slug.replace("-", " ").title()
                    
                    description = get_page_details(index_path)
                    icon = ICON_MAP.get(slug, DEFAULT_ICON)
                    
                    accidents.append({
                        "slug": slug,
                        "title": title,
                        "description": description,
                        "icon": icon
                    })
    
    # Sort alphabetically
    accidents.sort(key=lambda x: x["title"])
    print(f"Found {len(accidents)} accident types.")

    # 3. Build new grid HTML
    grid_html = ""
    for item in accidents:
        link = f"{item['slug']}/"
        grid_html += f"""
        <a class="group bg-white rounded-xl p-6 border border-gray-100 shadow-card hover:shadow-card-hover hover:border-primary/30 transition-all duration-300 flex flex-col h-full relative overflow-hidden"
            href="{link}">
            <div
                class="absolute top-0 left-0 w-1 h-full bg-primary transform scale-y-0 group-hover:scale-y-100 transition-transform origin-top duration-300">
            </div>
            <div
                class="w-12 h-12 rounded-lg bg-blue-50 text-primary flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-white transition-colors">
                <span class="material-symbols-outlined text-[28px]">{item['icon']}</span>
            </div>
            <h3 class="text-lg font-bold text-gray-900 mb-2 group-hover:text-primary transition-colors">
                {item['title']}</h3>
            <p class="text-sm text-text-muted leading-relaxed mb-4 flex-grow">{item['description']}</p>
            <div class="flex items-center text-sm font-semibold text-primary mt-auto">
                Leer guía <span
                    class="material-symbols-outlined text-[16px] ml-1 group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </div>
        </a>
        """

    # 4. Inject grid into the template
    # Existing grid has class including "gap-6"
    print("Replacing grid content...")
    grid_container = soup.find("div", class_="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6")
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
    generate_accidentes_index()
