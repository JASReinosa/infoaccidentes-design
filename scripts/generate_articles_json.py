
import os
import json
from bs4 import BeautifulSoup

ROOT_DIR = "."
OUTPUT_FILE = "js/articles.json"

TARGET_DIRS = ["guia", "indemnizacion", "reclamar-accidente"]

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

def get_page_details(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        # Title extraction
        h1 = soup.find("h1")
        title = h1.get_text(strip=True) if h1 else os.path.basename(os.path.dirname(file_path)).replace("-", " ").title()
        
        # Determine category based on directory
        rel_dir = os.path.relpath(os.path.dirname(file_path), ROOT_DIR)
        category = rel_dir.split(os.sep)[0].replace("-", " ").title()
        if category == "Guia": category = "Guía Legal"
        
        return title, category
    except Exception as e:
        print(f"Error parse {file_path}: {e}")
        return "Artículo", "General"

def generate_json_index():
    articles = []
    
    for target_dir in TARGET_DIRS:
        abs_target = os.path.join(ROOT_DIR, target_dir)
        if not os.path.exists(abs_target):
            continue
            
        for root, dirs, files in os.walk(abs_target):
            for file in files:
                if file == "index.html":
                    file_path = os.path.join(root, file)
                    
                    # Generate the relative URL from root
                    # logic: remove root_dir from path
                    rel_url = os.path.relpath(file_path, ROOT_DIR)
                    # For cleaner URLs, maybe remove index.html? internal linking usually keeps it or uses folder/.
                    # Let's keep the full path to avoid slash issues, or standardize on folder/
                    # Our site structure seems to rely on index.html being explicit in some places, 
                    # but let's see. The standardized links use index.html.
                    
                    # Wait, if we are in "guia/foo/index.html", simple href="guia/foo/index.html" works from root.
                    # But the JS will need to handle relative paths. 
                    # It's safest to store the absolute path from root (start with no slash or slash)
                    # and let the JS logic enable `../` prefixing calculation if needed, 
                    # OR we just store it as "guia/foo/index.html" and the JS helper 
                    # computes the right path based on current location.
                    
                    url = rel_url.replace("\\", "/")
                    
                    if url == "guia/index.html" or url == "indemnizacion/index.html" or url == "reclamar-accidente/index.html":
                         # Skip the section indexes themselves, we want articles
                         continue

                    title, category = get_page_details(file_path)
                    icon = get_icon_for_title(title)
                    
                    articles.append({
                        "title": title,
                        "url": url,
                        "category": category,
                        "icon": icon
                    })
    
    print(f"Found {len(articles)} articles.")
    
    # JS Template with embedded data
    js_content = f"""
const SITE_ARTICLES = {json.dumps(articles, ensure_ascii=False)};

document.addEventListener('DOMContentLoaded', function() {{
    const container = document.getElementById('related-articles-container');
    if (!container) return;
    
    // Helper to resolve root path based on depth
    // We look for the link to css/styles.css
    let rootPrefix = "";
    const cssLink = document.querySelector('link[href*="css/styles.css"]');
    if (cssLink) {{
        const href = cssLink.getAttribute('href');
        if (href.includes('css/styles.css')) {{
             rootPrefix = href.split('css/styles.css')[0];
        }}
    }}

    // Filter out current page
    const currentPath = window.location.pathname;
    const validArticles = SITE_ARTICLES.filter(article => {{
        // Basic check: if current path contains the article slug
        // article.url is like "guia/foo/index.html"
        const articleSlug = article.url.replace('/index.html', '');
        // handle both /foo/ and /foo/index.html in browser address
        return !currentPath.includes(articleSlug);
    }});
    
    if (validArticles.length === 0) return;
    
    // Pick 3 random
    const shuffled = validArticles.sort(() => 0.5 - Math.random());
    const selected = shuffled.slice(0, 3);
    
    // Render
    let html = `
     <h3 class="text-lg font-bold text-gray-900 mb-4 sticky top-0 bg-slate-50 z-10 py-2 border-b border-gray-200">
        Otros artículos de interés
     </h3>
     <div class="space-y-4">
    `;
    
    selected.forEach(article => {{
        const link = rootPrefix + article.url;
        // Generate fake view count: between 5k and 45k
        const views = (Math.floor(Math.random() * 40) + 5) + '.' + (Math.floor(Math.random() * 9)) + 'k';
        
        html += `
        <div class="flex flex-col gap-1 items-start group cursor-pointer border-b border-gray-100 pb-3 last:border-0 last:pb-0">
            <div>
                <h4 class="text-sm font-bold text-gray-900 group-hover:text-primary transition-colors line-clamp-2 leading-snug">
                    <a href="${{link}}" class="focus:outline-none">
                        <span class="absolute inset-0" aria-hidden="true"></span>
                        ${{article.title}}
                    </a>
                </h4>
                <div class="flex items-center gap-2 mt-1.5 text-xs">
                    <span class="text-ct-orange font-semibold text-orange-600 bg-orange-50 px-1.5 py-0.5 rounded flex items-center gap-1">
                        <span class="material-symbols-outlined text-[14px]">visibility</span>
                        ${{views}}
                    </span>
                    <span class="text-gray-400">•</span>
                    <span class="text-gray-500 uppercase tracking-wide opacity-80">
                        ${{article.category}}
                    </span>
                </div>
            </div>
            <a href="${{link}}" class="absolute inset-0" aria-hidden="true"></a>
        </div>
        `;
    }});
    
    html += `</div>`;
    container.innerHTML = html;
    container.classList.add("relative");
}});
"""

    # Save to JS file
    output_js_path = os.path.join(ROOT_DIR, "js/related-articles.js")
    os.makedirs(os.path.dirname(output_js_path), exist_ok=True)
    with open(output_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Generated {output_js_path} with {len(articles)} articles.")

if __name__ == "__main__":
    generate_json_index()
