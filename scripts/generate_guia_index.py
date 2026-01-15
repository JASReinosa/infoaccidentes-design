import os
from bs4 import BeautifulSoup

SOURCE_FILE = "reclamar-accidente/index.html"
TARGET_DIR = "guia"
TARGET_FILE = os.path.join(TARGET_DIR, "index.html")

def get_icon_for_title(title):
    t = title.lower()
    if any(x in t for x in ["seguro", "póliza", "consorcio", "cobertura", "mutua"]): return "security"
    if any(x in t for x in ["indemnización", "pago", "dinero", "cálculo", "cuantía", "cobrar", "lucro", "valor", "tributacion", "impuestos"]): return "payments"
    if any(x in t for x in ["lesión", "dolor", "latigazo", "secuela", "rehabilitación", "médico", "salud", "sanitario", "hospital", "baja", "forense", "biomecanica"]): return "medical_services"
    if any(x in t for x in ["legal", "ley", "delito", "juicio", "abogado", "reclamar", "denuncia", "demanda", "culpa", "responsable", "código penal", "defensa"]): return "gavel"
    if any(x in t for x in ["coche", "moto", "vehículo", "taller", "itv", "peritaje", "reparación", "siniestro", "autoescuela"]): return "directions_car"
    if any(x in t for x in ["policía", "atestado", "multa", "alcoholemia", "tráfico", "fuga"]): return "local_police"
    if any(x in t for x in ["patinete", "bici", "peatón", "andando", "atropello"]): return "directions_walk"
    if any(x in t for x in ["embarazo", "menor", "niño", "familiar"]): return "family_restroom"
    if any(x in t for x in ["documentacion", "parte", "papeles", "informe"]): return "description"
    return "article"

def fix_path_depth(path):
    if not path: return path
    if path.startswith(("http", "//", "#", "mailto:", "tel:")): return path
    if path.startswith("#"): return path
    
    # Source is depth 1 (reclamar-accidente/)
    # Target is depth 1 (guia/)
    # So paths starting with ../ are already correct.
    if path.startswith("../"): return path
    
    # "index.html" in the source refers to reclamar-accidente/index.html
    if path == "index.html": return "../reclamar-accidente/index.html"
    
    # Any other local path inside reclamar-accidente/ needs to go up and down?
    # But usually assets use ../
    
    return path

def get_page_details(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        # Try to find a good description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc else ""
        
        # If meta description is empty or default, try to read the first paragraph of content
        if not description or len(description) < 10:
             intro_p = soup.select_one("article p")
             if intro_p:
                 description = intro_p.get_text(strip=True)

        if not description:
            description = "Información detallada y consejos legales sobre este tema."

        # Truncate
        if len(description) > 120: description = description[:117] + "..."
        
        # Title extraction from H1
        h1 = soup.find("h1")
        title = h1.get_text(strip=True) if h1 else os.path.basename(os.path.dirname(file_path)).replace("-", " ").title()
        
        return title, description
    except Exception as e:
        print(f"Error parse {file_path}: {e}")
        return "Guía Legal", "Detalles sobre indemnizaciones y tráfico."

def generate_guia_index():
    print(f"Reading template {SOURCE_FILE}...")
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: {SOURCE_FILE} not found.")
        return
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Fix paths (Depth adjustment)
    print("Adjusting paths...")
    for tag in soup.find_all(['link', 'script', 'img', 'a']):
        if tag.name == 'link' and tag.get('href'): tag['href'] = fix_path_depth(tag['href'])
        elif tag.name == 'script' and tag.get('src'): tag['src'] = fix_path_depth(tag['src'])
        elif tag.name == 'img' and tag.get('src'): tag['src'] = fix_path_depth(tag['src'])
        elif tag.name == 'a' and tag.get('href'):
             tag['href'] = fix_path_depth(tag.get('href'))

    # 2. Customize Header/Hero for Blog context
    print("Customizing UI...")
    if soup.title: soup.title.string = "Blog Legal, Noticias y Guías - InfoAccidentes"
    
    # Hero Content
    hero_section = soup.find("section", class_="relative bg-white pt-16 pb-20 overflow-hidden")
    if hero_section:
        h1 = hero_section.find("h1")
        if h1:
            h1.clear()
            h1.append(BeautifulSoup('Biblioteca Legal: <span class="text-primary">Guías y Noticias</span>', "html.parser"))
        
        p = hero_section.find("p")
        if p: p.string = "Resuelve tus dudas legales. Todo sobre indemnizaciones, baremos, plazos y consejos para víctimas de accidentes."

    # Search Input
    search_input = soup.find("input", attrs={"placeholder": True})
    if search_input:
        search_input['placeholder'] = "Buscar en la biblioteca (ej. baremo 2026, latigazo, plazos...)"
        search_input['id'] = "searchInput"
        # Ensure it has a listener class just in case
        
    # Main Section Title
    main_section = soup.find("section", class_="py-16 bg-background-light border-t border-gray-100")
    if main_section:
        h2 = main_section.find("h2")
        if h2: h2.string = "Índice de Artículos y Guías"
        p_sub = main_section.find("p")
        if p_sub: p_sub.string = "Navega por nuestra colección completa de artículos ordenados alfabéticamente."

    # 3. Generate Content Grid
    print(f"Scanning {TARGET_DIR}...")
    items = []
    if os.path.exists(TARGET_DIR):
        with os.scandir(TARGET_DIR) as it:
            for entry in it:
                if entry.is_dir():
                    index_path = os.path.join(entry.path, "index.html")
                    if os.path.exists(index_path):
                        slug = entry.name
                        title, description = get_page_details(index_path)
                        icon = get_icon_for_title(title)
                        items.append((slug, title, description, icon))
    
    items.sort(key=lambda x: x[1]) # Sort alphabetically by title
    print(f"Found {len(items)} articles.")

    grid_html = ""
    for slug, title, desc, icon in items:
        link = f"{slug}/"
        # We add 'searchable-item' class and 'data-keywords' for the JS filter
        grid_html += f"""
        <article class="searchable-item group bg-white rounded-xl p-6 border border-gray-100 shadow-card hover:shadow-card-hover hover:border-primary/30 transition-all duration-300 flex flex-col h-full relative overflow-hidden" 
             data-keywords="{title.lower()} {slug.replace('-', ' ')}">
            <div class="absolute top-0 left-0 w-1 h-full bg-primary transform scale-y-0 group-hover:scale-y-100 transition-transform origin-top duration-300"></div>
            
            <div class="flex items-center justify-between mb-4">
                 <div class="w-12 h-12 rounded-lg bg-pink-50 text-pink-600 flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-colors">
                    <span class="material-symbols-outlined text-[24px]">{icon}</span>
                </div>
            </div>
            
            <h3 class="text-lg font-bold text-gray-900 mb-2 group-hover:text-primary transition-colors line-clamp-2 leading-tight">
                <a href="{link}" class="focus:outline-none">
                    <span class="absolute inset-0" aria-hidden="true"></span>
                    {title}
                </a>
            </h3>
            
            <p class="text-sm text-text-muted leading-relaxed mb-4 flex-grow line-clamp-3">
                {desc}
            </p>
            
            <div class="flex items-center text-sm font-semibold text-primary mt-auto">
                Leer más <span class="material-symbols-outlined text-[16px] ml-1 group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </div>
        </article>
        """

    # 4. Inject Grid
    print("Injecting grid...")
    grid_container = soup.find("div", class_=lambda x: x and "grid-cols-1" in x and "gap-6" in x)
    if grid_container:
        grid_container.clear()
        grid_container.append(BeautifulSoup(grid_html, "html.parser"))
        # Force a denser grid for blog posts (maybe 4 cols on XL)
        # The original class already has xl:grid-cols-4

    # 5. Inject Search Functionality
    print("Injecting JS...")
    js_script = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('searchInput');
        const items = document.querySelectorAll('.searchable-item');
        const container = document.querySelector('.grid');
        
        // Simple debouncing could be added but for 60 items instant is fine
        if (searchInput) {
            searchInput.addEventListener('input', function(e) {
                const term = e.target.value.toLowerCase().trim();
                let hasResults = false;
                
                items.forEach(item => {
                    const keywords = item.getAttribute('data-keywords') || '';
                    if (keywords.includes(term)) {
                        item.classList.remove('hidden');
                        hasResults = true;
                    } else {
                        item.classList.add('hidden');
                    }
                });
                
                // Optional: Show "No results" message if needed
            });
        }
    });
    </script>
    """
    soup.body.append(BeautifulSoup(js_script, "html.parser"))

    # Save
    os.makedirs(os.path.dirname(TARGET_FILE), exist_ok=True)
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
        
    print(f"Successfully generated {TARGET_FILE}")

if __name__ == "__main__":
    generate_guia_index()
