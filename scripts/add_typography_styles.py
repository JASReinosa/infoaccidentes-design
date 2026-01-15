
import os
from bs4 import BeautifulSoup

ROOT_DIR = "."

# Configuration
TAILWIND_CDN_OLD = "https://cdn.tailwindcss.com?plugins=forms,container-queries"
TAILWIND_CDN_NEW = "https://cdn.tailwindcss.com?plugins=forms,container-queries,typography"

PROSE_CLASSES = [
    "prose",
    "prose-lg", 
    "prose-slate", 
    "max-w-none",
    "prose-headings:font-bold", 
    "prose-headings:text-gray-900",
    "prose-p:text-gray-600", 
    "prose-p:leading-relaxed",
    "prose-a:text-cta-orange", 
    "prose-a:no-underline", 
    "hover:prose-a:underline",
    "prose-li:text-gray-600",
    "prose-strong:text-gray-900",
    "prose-strong:font-bold"
]

def update_typography():
    count_cdn = 0
    count_prose = 0
    
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
                    
                    # 1. Update CDN
                    script_tag = soup.find("script", src=lambda x: x and "cdn.tailwindcss.com" in x)
                    if script_tag and "typography" not in script_tag['src']:
                        script_tag['src'] = TAILWIND_CDN_NEW
                        changed = True
                        count_cdn += 1
                        
                    # 2. Add Prose Classes
                    # Target: <article> tags or main content divs
                    # In our templates, main content often has ID "articulo" or is an <article> tag
                    
                    # Priority 1: ID="articulo"
                    article_container = soup.find(id="articulo")
                    
                    # Priority 2: <article> tag
                    if not article_container:
                        article_container = soup.find("article")
                        
                    if article_container:
                        # Check if we need to apply classes
                        # Sometimes article_container contains the article text directly, or a wrapper
                        # Let's apply to the container itself if it's the right one.
                        
                        # Existing classes
                        current_classes = article_container.get("class", [])
                        
                        # Avoid double prose
                        if "prose" not in current_classes:
                            # We might need to go one level deeper if the container has "lg:w-2/3" etc
                            # In `accidente-patinete.html`, <main class="lg:w-2/3" id="articulo"> contains a DIV? 
                            # No, usually content is inside or in a wrapper.
                            # Let's check `accidente-patinete.html` structure:
                            # <main ... id="articulo"><div class="bg-slate-50 ...">... content ...</div></main>
                            # or <article class="prose ...">...</article>
                            
                            # If we find <article>, prefer that.
                            real_article = article_container.find("article")
                            if real_article:
                                target = real_article
                            else:
                                # Start applying prose to the container? 
                                # If the container has layout classes (grid cols), adding prose might break it?
                                # `prose` is usually safe as it styles children.
                                # But `prose` enforces max-width unless max-w-none is used.
                                
                                # Better strategy: Look for the specific content wrapper
                                # If `accidente-patinete.html` has <article class="prose..."> already in some places (from previous manual edits or template), skip.
                                
                                # Let's assume wetarget the element that *should* be prose.
                                # If `id="articulo"` is a `main` tag, it likely wraps the content.
                                
                                # Strategy: check if it has Prose. If not, add it.
                                target = article_container
                            
                            current_classes = target.get("class", [])
                            if "prose" not in current_classes:
                                # Merge classes
                                new_classes = current_classes + PROSE_CLASSES
                                # Deduplicate
                                target['class'] = list(set(new_classes)) 
                                # (set destroys order, but Tailwind doesn't care much, though standard sort is nice)
                                # Let's keep existing order + new
                                
                                final_classes = []
                                seen = set()
                                for c in current_classes + PROSE_CLASSES:
                                    if c not in seen:
                                        final_classes.append(c)
                                        seen.add(c)
                                        
                                target['class'] = final_classes
                                changed = True
                                count_prose += 1

                    if changed:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(soup.prettify())
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"Updated CDN in {count_cdn} files.")
    print(f"Added Typography classes to {count_prose} files.")

if __name__ == "__main__":
    update_typography()
