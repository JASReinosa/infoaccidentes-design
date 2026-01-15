
import csv
import os

CSV_FILE = "NUEVO-contenido_migracion_limpio_v2-html nuevo de las urls viejas - Nuevas URLs y Contenido HTML.csv"

def verify_all_pages():
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: CSV {CSV_FILE} not found.")
        return

    print(f"Total Rows in CSV: {len(rows)}")
    
    missing_pages = []
    found_count = 0
    skipped_count = 0 # Empty URLs or similar

    for i, row in enumerate(rows):
        url = row["URL Nueva"].strip()
        if not url:
            skipped_count += 1
            continue

        # Derive expected path
        path_suffix = url.replace("https://infoaccidentes.com/", "")
        if path_suffix.startswith("/"): path_suffix = path_suffix[1:]
        
        if path_suffix == "":
            path_suffix = "index.html"
        elif path_suffix.endswith("/"): 
            path_suffix += "index.html"
        elif not path_suffix.endswith(".html"): 
            path_suffix += "/index.html"
            
        full_path = os.path.abspath(path_suffix)
        
        if os.path.exists(full_path):
            found_count += 1
        else:
            missing_pages.append({
                "row": i + 2, # 1-based + header
                "url": url,
                "expected_path": path_suffix
            })

    print("-" * 30)
    print(f"Total Valid URLs: {len(rows) - skipped_count}")
    print(f"Pages Found: {found_count}")
    print(f"Pages Missing: {len(missing_pages)}")
    print("-" * 30)
    
    if missing_pages:
        print("MISSING PAGES:")
        for p in missing_pages:
            print(f"Row {p['row']}: {p['url']} -> {p['expected_path']}")

if __name__ == "__main__":
    verify_all_pages()
