
import re
import sys

file_path = 'index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Read {len(content)} bytes.")

# 1. Header
# Replace container class
content, n = re.subn(
    r'<div class="text-center mb-12">',
    '<div class="mb-12 flex flex-col md:flex-row justify-between items-end gap-4">',
    content
)
print(f"Header class replaced: {n}")

# Insert View All Link after <p>...</p> inside that div
# We find the new div start, then the p closing tag.
# Regex: (Selecciona tu caso[\s\S]*?</p>) -> \1 <link> </div> (Wait, existing div closing is preserved?)
# The previous replace didn't change the CLOSING div.
# So we insert the link before the closing div of that header.
# The header div contains h2 and p.
# We can search for the p block and append the link.
view_all_accidents = '''
       <a class="hidden md:flex items-center gap-2 text-primary font-bold hover:text-primary-dark transition-colors" href="reclamar-accidente/index.html">
        Ver todos los accidentes
        <span class="material-symbols-outlined">arrow_forward</span>
       </a>'''

content, n = re.subn(
    r'(Selecciona tu caso[\s\S]*?</p>)',
    r'\1' + view_all_accidents,
    content
)
print(f"Header link inserted: {n}")

# 2. Accident Items
# Match "In Itinere" block end.
# It ends with </a> followed by </div>.
# We look for "In\s+Itinere" ... "</a>"
new_accidents = '''
       <a class="group flex flex-col items-center p-6 bg-gray-50 rounded-xl border border-transparent hover:border-primary/30 hover:bg-white hover:shadow-md transition-all cursor-pointer" href="reclamar-accidente/bicicleta/index.html">
        <div class="w-14 h-14 rounded-full bg-primary/10 text-primary flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
         <span class="material-symbols-outlined text-3xl">
          pedal_bike
         </span>
        </div>
        <span class="font-bold text-text-dark group-hover:text-primary transition-colors">
         Bicicleta
        </span>
       </a>
       <a class="group flex flex-col items-center p-6 bg-gray-50 rounded-xl border border-transparent hover:border-primary/30 hover:bg-white hover:shadow-md transition-all cursor-pointer" href="reclamar-accidente/camion/index.html">
        <div class="w-14 h-14 rounded-full bg-primary/10 text-primary flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
         <span class="material-symbols-outlined text-3xl">
          local_shipping
         </span>
        </div>
        <span class="font-bold text-text-dark group-hover:text-primary transition-colors">
         Camión
        </span>
       </a>
       <a class="group flex flex-col items-center p-6 bg-gray-50 rounded-xl border border-transparent hover:border-primary/30 hover:bg-white hover:shadow-md transition-all cursor-pointer" href="reclamar-accidente/pasajero/index.html">
        <div class="w-14 h-14 rounded-full bg-primary/10 text-primary flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
         <span class="material-symbols-outlined text-3xl">
          airline_seat_recline_normal
         </span>
        </div>
        <span class="font-bold text-text-dark group-hover:text-primary transition-colors">
         Pasajero
        </span>
       </a>'''

# Regex for In Itinere end
content, n = re.subn(
    r'(In\s+Itinere[\s\S]*?</a>)',
    r'\1' + new_accidents,
    content
)
print(f"Accident items inserted: {n}")

# 3. Injury Items
# Match "Amputaciones" block end
new_injuries = '''
        <a class="flex items-center justify-between p-5 border-b border-gray-100 hover:bg-primary/5 transition-colors group" href="indemnizacion/hernia-discal/index.html">
         <div class="flex items-center gap-4">
          <span class="material-symbols-outlined text-muted group-hover:text-primary">
           accessibility_new
          </span>
          <span class="font-semibold text-lg text-text-dark">
           Hernia Discal
          </span>
         </div>
         <span class="material-symbols-outlined text-primary">
          chevron_right
         </span>
        </a>
        <a class="flex items-center justify-between p-5 border-b border-gray-100 hover:bg-primary/5 transition-colors group" href="indemnizacion/estres-postraumatico/index.html">
         <div class="flex items-center gap-4">
          <span class="material-symbols-outlined text-muted group-hover:text-primary">
           psychology
          </span>
          <span class="font-semibold text-lg text-text-dark">
           Estrés Postraumático
          </span>
         </div>
         <span class="material-symbols-outlined text-primary">
          chevron_right
         </span>
        </a>
        <a class="flex items-center justify-between p-5 hover:bg-primary/5 transition-colors group" href="indemnizacion/lesion-medular/index.html">
         <div class="flex items-center gap-4">
          <span class="material-symbols-outlined text-muted group-hover:text-primary">
           wheelchair_pickup
          </span>
          <span class="font-semibold text-lg text-text-dark">
           Lesión Medular
          </span>
         </div>
         <span class="material-symbols-outlined text-primary">
          chevron_right
         </span>
        </a>'''

content, n = re.subn(
    r'(Amputaciones[\s\S]*?</a>)',
    r'\1' + new_injuries,
    content
)
print(f"Injury items inserted: {n}")

# 4. Injury View All
# Insert after the closing </div> of the injury LIST.
# The previous regex inserted items INSIDE the list (because </a> is inside the list).
# So we need to find the `</div>` that closes the list.
# It is immediately after our new items (or last item).
# The list container is `<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">`
# We can search for that start tag, find the matching end tag?
# Easier: Just find the `</div>` that is followed by the Guía section.
# `</div>\s+<div class="flex flex-col gap-6">`
view_all_injuries = '''
       <div class="mt-4 text-center">
        <a class="inline-flex items-center gap-2 text-primary font-bold hover:text-primary-dark transition-colors" href="indemnizacion/index.html">
         Ver todas las lesiones
         <span class="material-symbols-outlined">arrow_forward</span>
        </a>
       </div>'''

content, n = re.subn(
    r'(</div>)(\s+<div class="flex flex-col gap-6">)',
    r'\1' + view_all_injuries + r'\2',
    content
)
print(f"Injury View All inserted: {n}")


# 5. Guide Items
# Match "Consorcio de Seguros" block end
new_guides = '''
       <div class="min-w-[260px] lg:min-w-0 snap-center bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col gap-3">
        <div class="flex items-start justify-between">
         <span class="material-symbols-outlined text-3xl text-primary">
          edit_document
         </span>
         <span class="text-xs font-bold text-primary bg-primary/10 px-2 py-1 rounded">
          LEGAL
         </span>
        </div>
        <h3 class="font-bold text-lg leading-tight">
         Parte Amistoso
        </h3>
        <p class="text-sm text-muted">
         Cómo rellenarlo correctamente para evitar problemas.
        </p>
        <a class="text-sm font-bold text-primary mt-auto flex items-center gap-1 hover:underline" href="guia/rellenar-parte-amistoso/index.html">
         Ver guía
         <span class="material-symbols-outlined text-base">
          arrow_forward
         </span>
        </a>
       </div>
       <div class="min-w-[260px] lg:min-w-0 snap-center bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col gap-3">
        <div class="flex items-start justify-between">
         <span class="material-symbols-outlined text-3xl text-primary">
          folder
         </span>
         <span class="text-xs font-bold text-primary bg-primary/10 px-2 py-1 rounded">
          INFO
         </span>
        </div>
        <h3 class="font-bold text-lg leading-tight">
         Documentación
        </h3>
        <p class="text-sm text-muted">
         Papeles necesarios para iniciar tu reclamación.
        </p>
        <a class="text-sm font-bold text-primary mt-auto flex items-center gap-1 hover:underline" href="guia/documentacion-reclamacion/index.html">
         Leer más
         <span class="material-symbols-outlined text-base">
          arrow_forward
         </span>
        </a>
       </div>
       <div class="min-w-[260px] lg:min-w-0 snap-center bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col gap-3">
        <div class="flex items-start justify-between">
         <span class="material-symbols-outlined text-3xl text-primary">
          work_history
         </span>
         <span class="text-xs font-bold text-primary bg-primary/10 px-2 py-1 rounded">
          SEGUROS
         </span>
        </div>
        <h3 class="font-bold text-lg leading-tight">
         Sin Baja Médica
        </h3>
        <p class="text-sm text-muted">
         ¿Es posible cobrar indemnización sin estar de baja?
        </p>
        <a class="text-sm font-bold text-primary mt-auto flex items-center gap-1 hover:underline" href="guia/indemnizacion-sin-baja/index.html">
         Descúbrelo
         <span class="material-symbols-outlined text-base">
          arrow_forward
         </span>
        </a>
       </div>'''

content, n = re.subn(
    r'(Consorcio de Seguros[\s\S]*?</a>\s+</div>)',
    r'\1' + new_guides,
    content
)
print(f"Guide items inserted: {n}")

# 6. Guide View All
# Match end of section
view_all_guides = '''
      <div class="mt-4 text-center lg:text-right">
       <a class="inline-flex items-center gap-2 text-primary font-bold hover:text-primary-dark transition-colors" href="guia/index.html">
        Ver todas las guías
        <span class="material-symbols-outlined">arrow_forward</span>
       </a>
      </div>
'''
content, n = re.subn(
    r'(</div>\s+</div>\s+</div>\s+</div>\s+</section>)',
    view_all_guides + r'\1',
    content
)
print(f"Guide View All inserted: {n}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("File written.")
