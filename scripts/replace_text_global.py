
import os

ROOT_DIR = "."
TARGET_TEXT = "clínicas concertadas UNESPA"
REPLACEMENT_TEXT = "clínicas"

def replace_text_global():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if TARGET_TEXT in content:
                        new_content = content.replace(TARGET_TEXT, REPLACEMENT_TEXT)
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        count += 1
                        # print(f"Updated {file}")
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    print(f"Replaced text in {count} files.")

if __name__ == "__main__":
    replace_text_global()
