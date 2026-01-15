
import os
from bs4 import BeautifulSoup
import re

ROOT_DIR = "."

def update_why_choose_us():
    count = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    if "accidente-patinete.html" in file:
                         print(f"DEBUG: Processing {file}")
                         
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    soup = BeautifulSoup(content, "html.parser")
                    changed = False
                    
                    # Find the "Por qué elegir" sidebar card
                    # It usually contains specific text or is a specific card structure
                    # We can look for the header text
                    
                    target_card = None
                    for h4 in soup.find_all(["h4", "h3"]):
                        if "Por qué elegir InfoAccidentes" in h4.get_text():
                            # The card is the parent container, usually a div
                            # Go up until we find the card div (bg-white/slate, rounded, etc)
                            parent = h4.parent
                            while parent and parent.name != "body":
                                # print(f"Checking parent {parent.name} with classes {parent.get('class', [])}")
                                if parent.name == "div" and any(c in parent.get("class", []) for c in ["rounded-xl", "rounded-lg", "shadow-lg", "border"]):
                                    target_card = parent
                                    # print(f"Found target card in {file}")
                                    break
                                parent = parent.parent
                            break
                    
                    if not target_card:
                        # print(f"No target card found in {file}")
                        pass
                    
                    if target_card:
                        if "accidente-patinete.html" in file:
                            print("DEBUG: Target card FOUND.")
                        
                        # Perform replacements on the HTML content of this card
                        # We do this by converting to string, replacing, and re-parsing?
                        # Or iterating nodes. String replacement is risky but easier for "sin coste" global in card.
                        
                        # Let's simple string replace on the formatted HTML of the card?
                        # BeautifulSoup modification is safer.
                        
                        # 1. Text Replacements
                        # "Especialistas en VMP" -> "Expertos en Accidentes de Tráfico"
                        # "abogados expertos en la nueva normativa de patinetes" -> "abogados expertos en toda España"
                        
                        for text_node in target_card.find_all(string=True):
                            original_text = str(text_node)
                            new_text = original_text
                            modified_node = False
                            
                            # Case insensitive replacement for specific phrases
                            # "Especialistas en VMP" -> "Expertos en Accidentes de Tráfico" (preserve case logic if needed, but here simple replace is intended for the specific phrase)
                            # Actually, text might vary slightly, but let's just make it case insensitive for the search phrase
                            
                            pattern1 = re.compile(r"Especialistas en VMP", re.IGNORECASE)
                            if pattern1.search(new_text):
                                new_text = pattern1.sub("Expertos en Accidentes de Tráfico", new_text)
                                modified_node = True
                                
                            pattern2 = re.compile(r"abogados expertos en la nueva normativa de patinetes", re.IGNORECASE)
                            if pattern2.search(new_text):
                                new_text = pattern2.sub("abogados expertos en toda España", new_text)
                                modified_node = True

                            # 2. Emphasis "sin coste" and "gratis"
                            # Handle multiline whitespace for "sin coste"
                            
                            # We need to render the HTML for the emphasis, so we pass new_text (string) to BeautifulSoup if we add tags.
                            # But wait, we are modifying the string content of a text node. 
                            # If we add spans, we need to replace the text node with a soup object/tag.
                            
                            # It's better to do the emphasis replacement on the string `new_text` as well,
                            # and if ANY change happened (text or emphasis), we replace the node.
                            
                            # Regex for highlighting
                            highlight_start = '<span class="font-black text-cta-orange uppercase">'
                            highlight_end = '</span>'
                            
                            # sin coste (allow whitespace including newlines)
                            pattern_coste = re.compile(r'(\bsin\s+coste\b)', re.IGNORECASE)
                            if pattern_coste.search(new_text):
                                # We need to verify we aren't doubly wrapping if ran multiple times
                                # But we iterate text nodes. Text nodes don't contain tags.
                                # So if we already wrapped it, "sin coste" is now inside a span, and the text node is just "sin coste" inside the span?
                                # No, find_all(string=True) returns text nodes.
                                # If we replaced "sin coste" with "<span>sin coste</span>", the parser sees a text node "sin coste" inside a span.
                                # So if we process that text node, we might wrap it again? 
                                # "sin coste" -> <span..>sin coste</span>.
                                # The text node "sin coste" is found. We wrap it -> <span..><span..>sin coste</span></span>.
                                # To avoid this, we should check parent.
                                
                                if text_node.parent.name != 'span' or "text-cta-orange" not in text_node.parent.get("class", []):
                                     new_text = pattern_coste.sub(f'{highlight_start}\\1{highlight_end}', new_text)
                                     modified_node = True
                                     
                            # gratis
                            pattern_gratis = re.compile(r'(\bgratis\b)', re.IGNORECASE)
                            if pattern_gratis.search(new_text):
                                 if text_node.parent.name != 'span' or "text-cta-orange" not in text_node.parent.get("class", []):
                                    new_text = pattern_gratis.sub(f'{highlight_start}\\1{highlight_end}', new_text)
                                    modified_node = True

                        # 3. Simplify "Defensa Jurídica" text
                        # Target specific h4 "Defensa Jurídica Gratuita" and update the following p
                        # Robust scanning (strip whitespace, case insensitive)
                        for h in target_card.find_all(["h4", "h5", "h3"]):
                            text = h.get_text(strip=True).lower()
                            if "defensajurídicagratuita" in text.replace(" ", "") or "defensajuridicagratuita" in text.replace(" ", ""):
                                # Found the header
                                p_tag = h.find_next("p")
                                if p_tag:
                                    # Replace content
                                    # Replace content
                                    # Use features="lxml" if available or just handle children
                                    # To be safe, just append the elements from the fragment
                                    new_content = 'Su defensa <span class="font-black text-primary uppercase">GRATIS</span>.' 
                                    frag = BeautifulSoup(new_content, "html.parser")
                                    
                                    p_tag.clear()
                                    if frag.body:
                                        for child in list(frag.body.children):
                                            p_tag.append(child)
                                    else:
                                        for child in list(frag.children):
                                            p_tag.append(child)
                                            
                                    changed = True
                                    if "accidente-patinete.html" in file:
                                        print(f"DEBUG: Text replaced. New p_tag: {p_tag}")

                        # 4. Change Highlight Color (Orange -> Blue) in this card
                        # Find all spans with text-cta-orange in this card and swap to text-primary
                        for span in target_card.find_all("span"):
                            classes = span.get("class", [])
                            if "text-cta-orange" in classes:
                                classes.remove("text-cta-orange")
                                if "text-primary" not in classes:
                                    classes.append("text-primary")
                                span['class'] = classes
                                changed = True
                                if "accidente-patinete.html" in file:
                                    print("DEBUG: Color updated.")
                        count += 1
                        
                    if changed:
                        if "accidente-patinete.html" in file:
                            print(f"DEBUG: Soup checks - Has 'Su defensa': {'Su defensa' in soup.prettify()}")

                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(soup.prettify())
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"Updated 'Why Choose Us' content in {count} files.")

if __name__ == "__main__":
    update_why_choose_us()
