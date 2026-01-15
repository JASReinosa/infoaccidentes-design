
import sys

file_path = 'index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Header
target_header = '''      <div class="text-center mb-12">
       <h2 class="text-3xl md:text-4xl font-bold text-text-dark mb-4 tracking-tight">
        ¿Qué tipo de accidente
                        has tenido?
       </h2>
       <p class="text-muted text-lg">
        Selecciona tu caso para recibir asesoramiento personalizado
       </p>
      </div>'''

replacement_header = '''      <div class="mb-12 flex flex-col md:flex-row justify-between items-end gap-4">
       <div class="text-left">
        <h2 class="text-3xl md:text-4xl font-bold text-text-dark mb-4 tracking-tight">
         ¿Qué tipo de accidente
         <span class="block text-primary">has tenido?</span>
        </h2>
        <p class="text-muted text-lg">
         Selecciona tu caso para recibir asesoramiento personalizado
        </p>
       </div>
       <a class="hidden md:flex items-center gap-2 text-primary font-bold hover:text-primary-dark transition-colors" href="reclamar-accidente/index.html">
        Ver todos los accidentes
        <span class="material-symbols-outlined">arrow_forward</span>
       </a>
      </div>'''

if target_header in content:
    content = content.replace(target_header, replacement_header)
    print("Header updated.")
else:
    print("Header TARGET NOT FOUND.")
    # Debug: print snippet
    start = content.find("¿Qué tipo de accidente")
    if start != -1:
        print(f"Header snippet found at {start}, but full block mismatch.")
        print(repr(content[start-50:start+150]))

# 2. Accident Items
target_accidents = '''       <a class="group flex flex-col items-center p-6 bg-gray-50 rounded-xl border border-transparent hover:border-primary/30 hover:bg-white hover:shadow-md transition-all cursor-pointer" href="#">
        <div class="w-14 h-14 rounded-full bg-primary/10 text-primary flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
         <span class="material-symbols-outlined text-3xl">
          work
         </span>
        </div>
        <span class="font-bold text-text-dark group-hover:text-primary transition-colors">
         In
                             Itinere
        </span>
       </a>'''

replacement_accidents = target_accidents + '''
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

if target_accidents in content:
    content = content.replace(target_accidents, replacement_accidents)
    print("Accident items added.")
else:
    print("Accident items TARGET NOT FOUND.")

# 3. Injury Items
target_injuries = '''         <a class="flex items-center justify-between p-5 hover:bg-primary/5 transition-colors group" href="#">
          <div class="flex items-center gap-4">
           <span class="material-symbols-outlined text-muted group-hover:text-primary">
            accessible
           </span>
           <span class="font-semibold text-lg text-text-dark">
            Amputaciones
           </span>
          </div>
          <span class="material-symbols-outlined text-primary">
           chevron_right
          </span>
         </a>
        </div>'''

replacement_injuries = '''         <a class="flex items-center justify-between p-5 hover:bg-primary/5 transition-colors group" href="#">
          <div class="flex items-center gap-4">
           <span class="material-symbols-outlined text-muted group-hover:text-primary">
            accessible
           </span>
           <span class="font-semibold text-lg text-text-dark">
            Amputaciones
           </span>
          </div>
          <span class="material-symbols-outlined text-primary">
           chevron_right
          </span>
         </a>
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
        </a>
       </div>
       <div class="mt-4 text-center">
        <a class="inline-flex items-center gap-2 text-primary font-bold hover:text-primary-dark transition-colors" href="indemnizacion/index.html">
         Ver todas las lesiones
         <span class="material-symbols-outlined">arrow_forward</span>
        </a>
       </div>'''

if target_injuries in content:
    content = content.replace(target_injuries, replacement_injuries)
    print("Injury items added.")
else:
    print("Injury items TARGET NOT FOUND.")

# 4. Guide Items
# This one is tricky because it's long.
# I'll match the "Consorcio de Seguros" header and replace the block?
# Or clearer: match the block starting from the Consorcio div.
target_guides_start = '''         <div class="min-w-[260px] lg:min-w-0 lg:col-span-2 snap-center bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col gap-3">
          <div class="flex items-start justify-between">
           <span class="material-symbols-outlined text-3xl text-primary">
            shield
           </span>'''
# Just verify this unique start exists.
if target_guides_start in content:
    # Find the closing div for this block.
    start_wrapper_idx = content.find(target_guides_start)
    # The block ends with </a> followed by </div>.
    # We can perform a replace on the substring if we knew the exact content.
    # Let's assume we can construct the exact string.
    # The variable content varies.
    # Let's search for "Consorcio de Seguros"
    consorcio_idx = content.find('Consorcio de Seguros', start_wrapper_idx)
    # Find the closing </div> of this item.
    # It follows </a>.
    end_item_idx = content.find('</div>', content.find('</a>', consorcio_idx)) + 6
    
    # We will insert new items AFTER this index.
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
    
    content = content[:end_item_idx] + new_guides + content[end_item_idx:]
    print("Guide items added.")
    
    # Guide View All
    # Add after the container closes.
    # The container closes at `</div>` followed by `</div>`.
    # It was originally:
    # ... </div> (Consorcio)
    # </div> (Container)
    # </div> (Col)
    # After insertion:
    # ... </div> (Sin Baja)
    # </div> (Container)
    # We need to find the next `</div>` after our new insertion point.
    container_end_idx = content.find('</div>', end_item_idx + len(new_guides)) + 6
    
    view_all_guides = '''
      <div class="mt-4 text-center lg:text-right">
       <a class="inline-flex items-center gap-2 text-primary font-bold hover:text-primary-dark transition-colors" href="guia/index.html">
        Ver todas las guías
        <span class="material-symbols-outlined">arrow_forward</span>
       </a>
      </div>'''
      
    content = content[:container_end_idx] + view_all_guides + content[container_end_idx:]
    print("Guide View All added.")

else:
    print("Guide items TARGET NOT FOUND.")


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
