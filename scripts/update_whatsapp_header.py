
import os
from bs4 import BeautifulSoup
import re

# WhatsApp Icon SVG path data
WA_PATH_D = "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"

def update_files():
    root_dir = "."
    files_processed = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip node_modules and hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    soup = BeautifulSoup(content, "html.parser")
                    changed = False
                    
                    # Find all links that go to whatsapp and contain "24h" or use "bg-cta-orange"
                    # Strategy: look for links with api.whatsapp.com
                    # Then filter for the ones in the header (nav/header context preferably, but the URL is unique enough + btn style)
                    
                    links = soup.find_all("a", href=lambda x: x and "api.whatsapp.com" in x)
                    
                    for link in links:
                        # Check text content
                        text = link.get_text(strip=True)
                        if "WhatsApp 24h" in text:
                            # Verify if it is one of the target buttons by class or presence of material icon
                            classes = link.get("class", [])
                            
                            # Check for Desktop properties
                            is_desktop = "bg-cta-orange" in classes and "hover:bg-cta-orange-hover" in classes and "rounded-lg" in classes
                            
                            # Check for Mobile properties
                            is_mobile = "bg-cta-orange" in classes and "w-full" in classes and "text-white" in classes
                            
                            if is_desktop or is_mobile:
                                # 1. Update Classes
                                # Remove orange classes
                                if "bg-cta-orange" in classes: classes.remove("bg-cta-orange")
                                if "hover:bg-cta-orange-hover" in classes: classes.remove("hover:bg-cta-orange-hover")
                                
                                # Add green classes (using Tailwind arbitrary values for exact hex match as requested/inferred)
                                # Or add a class if defined. I'll use arbitrary values for safety: bg-[#25D366] hover:bg-[#20bd5a]
                                new_classes = classes + ["bg-[#25D366]", "hover:bg-[#20bd5a]"]
                                link['class'] = new_classes
                                
                                # 2. Update Content (Icon + Text)
                                link.clear()
                                
                                # Create SVG Icon
                                svg = soup.new_tag("svg", xmlns="http://www.w3.org/2000/svg", viewBox="0 0 24 24")
                                svg['class'] = "w-5 h-5 fill-current"
                                path = soup.new_tag("path", d=WA_PATH_D)
                                svg.append(path)
                                
                                # Append content
                                link.append(svg)
                                link.append(" WhatsApp") # Add space before text for visual separation if gap not enough? 
                                # Actually flex gap-2 is present in parent. " WhatsApp" string is handled as text node.
                                
                                # The original had text node "WhatsApp 24h"
                                # We want just "WhatsApp" (as a text node)
                                # Note: soup.new_tag is for tags. accessing link.append(" string") works for text.
                                # But we need to ensure whitespace if needed. The container has gap-2.
                                
                                changed = True

                    if changed:
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(soup.prettify())
                        files_processed += 1
                        print(f"Updated: {full_path}")
                        
                except Exception as e:
                    print(f"Error processing {full_path}: {e}")

    print(f"Total files updated: {files_processed}")

if __name__ == "__main__":
    update_files()
