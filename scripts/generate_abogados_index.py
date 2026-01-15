
import os
from bs4 import BeautifulSoup
import copy

SOURCE_FILE = "abogados.html"
TARGET_DIR = "abogados-trafico"
TARGET_FILE = os.path.join(TARGET_DIR, "index.html")

def fix_path_depth(path):
    if not path: return path
    if path.startswith(("http", "//", "#", "mailto:", "tel:")): return path
    # If it's already relative (starts with ../), we might need to adjust, 
    # but the source file is in root, so all paths are either absolute or relative to root.
    # We are moving 1 level deep, so we just prepend ../
    
    # Check if it's an anchor link on the same page
    if path.startswith("#"): return path
    
    return "../" + path

def generate_abogados_index():
    print(f"Reading {SOURCE_FILE}...")
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: {SOURCE_FILE} not found.")
        return

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Update relative paths for depth change (Root -> /abogados-trafico/)
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
            if original_href == "abogados.html":
                tag['href'] = "index.html" # Self reference
            else:
                tag['href'] = fix_path_depth(original_href)

    # 2. explicit fix for the logo link and nav links if they were just "index.html"
    # fix_path_depth("index.html") -> "../index.html" which is correct for home.

    # 3. Generate Directory List
    print(f"Scanning {TARGET_DIR} for cities...")
    cities = []
    if os.path.exists(TARGET_DIR):
        for entry in os.scandir(TARGET_DIR):
            if entry.is_dir():
                # Check for index.html inside
                if os.path.exists(os.path.join(entry.path, "index.html")):
                    city_slug = entry.name
                    city_name = city_slug.replace("-", " ").title()
                    cities.append((city_name, city_slug))
    
    cities.sort()
    print(f"Found {len(cities)} cities.")

    # 4. Create Directory Section
    directory_html = """
    <section id="directorio" class="py-20 bg-white border-t border-slate-200">
        <div class="mx-auto max-w-7xl px-6 lg:px-8">
            <div class="mb-12 text-center">
                <h2 class="text-3xl font-bold tracking-tight text-text-main">Directorio Completo de Abogados</h2>
                <p class="mt-2 text-text-secondary">Encuentra especialistas en tu localidad</p>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
    """
    
    for name, slug in cities:
        # Link is relative to abogados-trafico/index.html, so "./slug/" or "slug/"
        link = f"{slug}/" 
        directory_html += f"""
                <a href="{link}" class="group flex items-center p-3 rounded-lg hover:bg-slate-50 transition-colors border border-transparent hover:border-slate-100">
                    <span class="material-symbols-outlined text-slate-300 group-hover:text-primary mr-2 text-lg">location_on</span>
                    <span class="text-sm font-medium text-text-main group-hover:text-primary">{name}</span>
                </a>
        """
    
    directory_html += """
            </div>
        </div>
    </section>
    """
    
    # 5. Inject Directory Section before Footer
    # Find footer
    footer = soup.find("footer")
    if footer:
        directory_soup = BeautifulSoup(directory_html, "html.parser")
        footer.insert_before(directory_soup)
    else:
        print("Warning: Footer not found, appending directory at end of body.")
        if soup.body:
            soup.body.append(BeautifulSoup(directory_html, "html.parser"))

    # 6. Update "Ver listado completo" link
    # The button text is "Ver listado completo"
    # We look for an <a> containing this text
    target_link = None
    for a in soup.find_all("a"):
        if "Ver listado completo" in a.get_text():
            target_link = a
            break
            
    if target_link:
        target_link['href'] = "#directorio"
        print("Updated 'Ver listado completo' link target.")
    else:
        print("Warning: 'Ver listado completo' link not found.")
        
    # 7. Save
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
        
    print(f"Successfully generated {TARGET_FILE}")

if __name__ == "__main__":
    generate_abogados_index()
