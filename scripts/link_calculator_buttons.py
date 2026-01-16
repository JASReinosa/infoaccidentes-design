import os
import re
from bs4 import BeautifulSoup
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/macniacos/infoaccidentes-design")
TARGET_CALC_DIR = "calculadora-indemnizacion"
TARGET_CALC_FILE = "index.html"
KEYWORDS = [r"calcular", r"calcula", r"cálculo", r"indemnizac", r"cuánto", r"cuanto"]

def get_relative_path(from_file, to_dir, to_file):
    """
    Calculates the relative path from a source file to the target file.
    """
    from_file_path = Path(from_file).resolve()
    target_path = (PROJECT_ROOT / to_dir / to_file).resolve()
    
    try:
        rel_path = os.path.relpath(target_path, from_file_path.parent)
        return rel_path
    except ValueError:
        return None

def is_button_or_cta(tag):
    """
    Checks if an <a> tag looks like a button or CTA based on classes.
    """
    classes = tag.get("class", [])
    if isinstance(classes, str):
        classes = classes.split()
    
    button_classes = ["btn", "button", "cta", "bg-", "rounded", "shadow", "text-white", "font-bold"]
    
    for cls in classes:
        for btn_cls in button_classes:
            if btn_cls in cls:
                return True
                
    if tag.has_attr("style"):
        style = tag["style"].lower()
        if "background" in style or "padding" in style or "border" in style:
            return True

    return False

def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")
        modified = False
        
        # Find all <a> tags
        for a in soup.find_all("a"):
            text = a.get_text(strip=True).lower()
            href = a.get("href", "")
            
            # Check if it points to calculator (exact or relative)
            is_calculator_link = False
            if "calculadora-indemnizacion/index.html" in href:
                is_calculator_link = True
            
            # Process Keywords if not already a calculator link (to catch missed ones) OR if it IS one (to clean it)
            keyword_match = any(re.search(k, text, re.IGNORECASE) for k in KEYWORDS)
            
            should_be_calculator = is_calculator_link or (keyword_match and is_button_or_cta(a))
            
            if should_be_calculator:
                # 1. Update HREF if needed (ensure correct relative path)
                if not is_calculator_link: # Only update path if it wasn't already pointing there
                     rel_path = get_relative_path(file_path, TARGET_CALC_DIR, TARGET_CALC_FILE)
                     if rel_path and href != rel_path:
                        print(f"LINK UPDATE: {file_path} -> '{text[:20]}' -> {rel_path}")
                        a["href"] = rel_path
                        modified = True
                        is_calculator_link = True # Now it is one

                # 2. Cleanup Attributes (target, rel) for internal calculator links
                if is_calculator_link:
                    if a.has_attr("target") and a["target"] == "_blank":
                        print(f"FIX ATTRIB: {file_path} -> Removed target='_blank'")
                        del a["target"]
                        modified = True
                    
                    if a.has_attr("rel"):
                        # Remove 'noopener' and 'noreferrer' if present
                        rels = a["rel"]
                        if isinstance(rels, str):
                            rels = rels.split()
                        
                        new_rels = [r for r in rels if r not in ["noopener", "noreferrer"]]
                        
                        if len(new_rels) != len(rels):
                            if not new_rels:
                                del a["rel"]
                            else:
                                a["rel"] = new_rels
                            modified = True

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(str(soup))
            return True
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    count = 0
    for root, _, files in os.walk(PROJECT_ROOT):
        if ".git" in root or ".gemini" in root or "node_modules" in root:
            continue
            
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                if process_file(file_path):
                    count += 1
    
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    main()
