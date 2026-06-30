# Estrategia de Reconstrucción SEO y Auditoría Digital - InfoAccidentes

Este documento recopila la información estratégica extraída de NotebookLM para guiar el rediseño y la reconstrucción técnica de **infoaccidentes.com**. Su objetivo es posicionar la web estática como el referente líder de captación de leads en España para lesionados de accidentes.

---

## 1. Auditoría Digital de Semrush y Analítica

El análisis técnico revela problemas significativos en el rendimiento, rastreo y estructura del sitio que deben corregirse:

* **Errores Críticos (35 en total):**
  * **Schema inválido:** 18 elementos de datos estructurados (Schema) incorrectos que impiden mostrar *rich snippets* en las búsquedas.
  * **Hreflang:** 16 conflictos con las etiquetas `hreflang` en el código fuente.
  * **Sitemap:** 1 URL incorrecta en el `sitemap.xml`.
* **Advertencias de Rendimiento y Rastreo (706 en total):**
  * **WPO:** Más de 500 advertencias debido a archivos JavaScript y CSS no cacheados o no minificados.
  * **Robots.txt:** 142 recursos internos bloqueados para rastreadores.
  * **Ratio de Texto/HTML:** 14 páginas con una proporción de texto muy baja debido a maquetadores visuales pesados.
  * **Encabezados:** Páginas con etiquetas H1 duplicadas o ausentes.
* **Avisos Menores (34 en total):**
  * 15 páginas bloqueadas para rastreo.
  * Advertencias por redirecciones permanentes múltiples.
  * 5 páginas con un solo enlace interno entrante (páginas huérfanas o con baja autoridad).
* **Secuelas del Ataque Web:**
  * Tráfico extranjero irrelevante en GA4 importado de Search Console.
  * Miles de URLs basura bajo el directorio `/debate/` que deben eliminarse forzando un código de error HTTP **404** o **410** definitivo.

---

## 2. Pautas de Rediseño: UX/UI y Marca

El nuevo diseño estático (Tailwind) debe solucionar los problemas de usabilidad e integrar la nueva identidad de marca:

* **Identidad Visual y Mensaje:**
  * **Paleta de Colores:** Alejarse del naranja y usar una paleta basada en el **azul corporativo**, inspirada en las señales de tráfico informativas españolas.
  * **Logotipo:** Minimalista y cercano, transformando la "i" en un signo de exclamación (advertencia/información).
  * **Eslogan:** *"Piensa en ti, nosotros ya lo hacemos. Si pasa algo, nos ocuparemos de todo."*
* **Limpieza de Código:**
  * Eliminar la excesiva profundidad del DOM generada previamente por Elementor (divs vacíos, márgenes innecesarios).
  * Unificar estilos tipográficos para párrafos (`<p>`).
  * Evitar saltos de línea forzados (`<br>`) en favor del uso de márgenes CSS correctos.
  * Utilizar listas (`<ul>`, `<li>`) y negritas (`<strong>`) para optimizar la legibilidad en pantallas móviles.
* **Jerarquía de Encabezados:**
  * Corregir el salto abrupto de H1 a H3. El flujo semántico correcto debe respetarse (H1 -> H2 -> H3).
* **Atribución en GA4:**
  * Eliminar el uso incorrecto de `target="_blank"` con `rel="noreferrer"` en enlaces que apuntan a nuestro propio dominio, ya que rompe las sesiones en Google Analytics 4 (atribución errónea).
* **SEO Local:**
  * Crear y verificar el Perfil de Empresa en Google (Google Business Profile) para aparecer en Google Maps al buscar "Info Accidentes".

---

## 3. Estrategia de Reconstrucción SEO

La web antigua sufre de **canibalización masiva y duplicidad geográfica** (ej. múltiples URLs de clínicas en una misma ciudad), permalinks desordenados con sufijos "-2" y contenido redundante.

### Estructura en Silos
El sitio se organizará en las siguientes verticales lógicas y limpias de contenido:
1. **Abogados** (Silo Legal)
2. **Clínicas** (Silo Médico)
3. **Tipo de Vehículo**
4. **Lesiones**
5. **Herramientas** (Calculadora de Indemnización)
6. **Guías/Blog**

### Consolidación de URLs
* Fusionar las múltiples URLs duplicadas por intención de búsqueda en **una única URL maestra**. Por ejemplo, todas las clínicas en Madrid se concentrarán exclusivamente en: `https://infoaccidentes.com/clinicas-accidentes-trafico/madrid/`.

### Plan de Acción de 3 Pasos
1. **La "Gran Consolidación" (Redirecciones 301):** Crear un mapa de redirecciones exhaustivo para canalizar el "link juice" de las páginas canibalizadas hacia la nueva URL principal de cada silo o ciudad.
2. **Poda de Contenido (Content Pruning):** Eliminar URLs redundantes, unificar calculadoras duplicadas en una "Calculadora Definitiva" y redirigir políticas legales desactualizadas.
3. **Enlazado Interno Estratégico:** La Home apuntará a los Silos principales, los Silos a las subpáginas locales (ciudades/provincias) y las guías informativas del blog enlazaran a los servicios transaccionales y calculadoras para maximizar la conversión.

### Estrategia de CTAs (Llamadas a la Acción)
Clasificar los botones por nivel de urgencia:
* **Alta Urgencia:** *"¡Reclama tu Indemnización Máxima AHORA!"* o *"Consulta Legal GRATUITA"*. Se posicionarán en zonas calientes (*above the fold*) o en banners flotantes.
* **Urgencia Media:** Enlaces a las calculadoras para captar leads que aún están calculando la viabilidad de su caso.
* **Baja Urgencia:** Descargas de Guías informativas o suscripciones a cambio de datos (*lead magnets*).
