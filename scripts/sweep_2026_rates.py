import os

ROOT_DIR = "."

REPLACEMENTS = {
    # 2.9% IPC update for 2026 daily rates (comma formats)
    "39,13 €": "39,20 €",
    "67,82 €": "67,96 €",
    "97,83 €": "98,02 €",
    "130,44 €": "130,69 €",
    
    "39,13€": "39,20€",
    "67,82€": "67,96€",
    "97,83€": "98,02€",
    "130,44€": "130,69€",
    
    # Dot formats
    "39.13 €": "39.20 €",
    "67.82 €": "67.96 €",
    "97.83 €": "98.02 €",
    "130.44 €": "130.69 €",
    
    "39.13€": "39.20€",
    "67.82€": "67.96€",
    "97.83€": "98.02€",
    "130.44€": "130.69€",
    
    # Text mentions of individual numbers
    " 39,13": " 39,20",
    " 67,82": " 67,96",
    " 97,83": " 98,02",
    " 130,44": " 130,69",
    
    # Revalorization percentage
    "2,7%": "2,9%",
    "2.7%": "2.9%",
    "2,7 %": "2,9 %",
    "2.7 %": "2.9 %",
    
    # Surgical rates revalorization
    "521,75 €": "536,88 €",
    "2.086,99 €": "2.147,51 €",
    "521,75€": "536,88€",
    "2.086,99€": "2.147,51€"
}

def sweep_rates():
    print("Iniciando barrido de coherencia de tarifas Baremo 2026 (subida oficial del 2,9%)...")
    count = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip legacy and system folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'legacy', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    original_content = content
                    for old_val, new_val in REPLACEMENTS.items():
                        content = content.replace(old_val, new_val)
                    
                    if content != original_content:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        count += 1
                        # print(f"Actualizadas tarifas en: {file_path}")
                        
                except Exception as e:
                    print(f"Error procesando {file_path}: {e}")
                    
    print(f"Barrido completado. Total archivos HTML actualizados con tarifas 2026 coherentes: {count}")

if __name__ == "__main__":
    sweep_rates()
