import os
import re
import argparse
from bs4 import BeautifulSoup

def inject_gtm(gtm_id="GTM-XXXXXXX", sgtm_domain="sst.infoaccidentes.com", root_dir="."):
    print(f"Preparando inyección de GTM...")
    print(f"ID del contenedor: {gtm_id}")
    print(f"Dominio Server-Side: {sgtm_domain}")

    # GTM Script template to insert in <head>
    head_script_str = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://{sgtm_domain}/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{gtm_id}');</script>
<!-- End Google Tag Manager -->"""

    # GTM Noscript template to insert in <body>
    body_noscript_str = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://{sgtm_domain}/ns.html?id={gtm_id}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

    count = 0
    for root, dirs, files in os.walk(root_dir):
        # Exclude system folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'scripts', '__pycache__']]
        
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Check if GTM is already injected
                    if "Google Tag Manager" in content:
                        # If GTM is already there, we update the GTM ID and domain
                        # This allows re-running the script to update the IDs later
                        content_updated = re.sub(
                            r'https://[^/]+/gtm\.js\?id=GTM-[A-Z0-9]+',
                            f'https://{sgtm_domain}/gtm.js?id={gtm_id}',
                            content
                        )
                        content_updated = re.sub(
                            r'https://[^/]+/ns\.html\?id=GTM-[A-Z0-9]+',
                            f'https://{sgtm_domain}/ns.html?id={gtm_id}',
                            content_updated
                        )
                        content_updated = re.sub(
                            r"'\bGTM-[A-Z0-9]+\b'",
                            f"'{gtm_id}'",
                            content_updated
                        )
                        
                        if content_updated != content:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(content_updated)
                            print(f"GTM actualizado en: {file_path}")
                        continue

                    # Fresh injection
                    soup = BeautifulSoup(content, "html.parser")
                    
                    # Parse scripts into BeautifulSoup objects
                    head_soup = BeautifulSoup(head_script_str, "html.parser")
                    body_soup = BeautifulSoup(body_noscript_str, "html.parser")
                    
                    # Inject in <head>
                    if soup.head:
                        # Insert at the absolute top of head
                        soup.head.insert(0, head_soup)
                    else:
                        print(f"Advertencia: No se encontró <head> en {file_path}")
                        continue
                        
                    # Inject in <body>
                    if soup.body:
                        # Insert at the absolute top of body
                        soup.body.insert(0, body_soup)
                    else:
                        print(f"Advertencia: No se encontró <body> en {file_path}")
                        continue
                        
                    # Write file back
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(soup.prettify())
                    
                    count += 1
                    # print(f"GTM Inyectado en: {file_path}")
                    
                except Exception as e:
                    print(f"Error procesando {file_path}: {e}")

    print(f"Inyección finalizada. Total archivos HTML procesados: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inyecta o actualiza Google Tag Manager en archivos HTML.")
    parser.add_argument("--id", default="GTM-XXXXXXX", help="ID del contenedor de GTM (ej. GTM-W9XYZ12)")
    parser.add_argument("--domain", default="sst.infoaccidentes.com", help="Dominio de sGTM (ej. sst.infoaccidentes.com)")
    parser.add_argument("--dir", default=".", help="Directorio raíz para buscar archivos HTML")
    args = parser.parse_args()
    
    inject_gtm(gtm_id=args.id, sgtm_domain=args.domain, root_dir=args.dir)
