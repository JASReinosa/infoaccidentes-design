# Plan de Medición y Arquitectura de dataLayer (Server-Side GTM) - InfoAccidentes

Este documento define la estructura de eventos del `dataLayer` que se inyectarán en la web estática para permitir una medición avanzada mediante **Google Tag Manager (Server-Side)**. El objetivo principal es optimizar la atribución de conversión en campañas (Google Ads, Meta Ads) y trackear el embudo de conversión para mejorar la calidad y volumen de los leads.

---

## 1. Configuración de GTM Server-Side (Carga First-Party)

Para evitar bloqueos de ad-blockers, cargaremos GTM desde nuestro subdominio de tracking (ej: `sst.infoaccidentes.com`).

### Código del Head
```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://sst.infoaccidentes.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
```

### Código del Body
```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://sst.infoaccidentes.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

---

## 2. Eventos del `dataLayer` recomendados para Growth Hacking

### Evento 1: Inicio del Embudo de la Calculadora (`calc_start`)
Se dispara cuando el usuario interactúa con la primera opción del formulario.
* **Propósito:** Medir la tasa de inicio del embudo.
```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'event': 'calc_start',
  'calc_role_initial': 'conductornoculpa' // Opcion por defecto
});
```

### Evento 2: Avance del Paso (`calc_step_complete`)
Se dispara cuando el usuario pulsa "Siguiente" en cada paso.
* **Propósito:** Analizar fugas del embudo (paso 1 al 2, paso 2 al 3).
```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'event': 'calc_step_complete',
  'calc_step_number': 1, // 1, 2 o 3
  'calc_step_name': 'tipo_accidente' // tipo_accidente, tiempo_recuperacion, secuelas
});
```

### Evento 3: Cálculo Completado (`calc_complete`)
Se dispara cuando el usuario hace clic en "Calcular Indemnización" y ve el resultado estimado.
* **Propósito:** Registrar un lead calificado "blando". Guardamos los datos médicos de forma anónima para segmentación.
```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'event': 'calc_complete',
  'calc_estimated_range': '3.200€ - 4.500€',
  'calc_days_uci': 0,
  'calc_days_hospital': 2,
  'calc_days_baja': 30,
  'calc_days_rehab': 15,
  'calc_severity': 'light',
  'calc_victim_age': 35,
  'calc_province': 'cantabria'
});
```

### Evento 4: Conversión Principal - WhatsApp Click (`lead_whatsapp`)
Se dispara cuando el usuario hace clic en "Recibir valoración oficial por WhatsApp" en el resultado final o en el menú cabecera/flotante.
* **Propósito:** Conversión de venta directa (Lead Calificado "Duro").
```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'event': 'lead_whatsapp',
  'lead_source': 'calculator_result', // 'header', 'calculator_result', 'floating_button'
  'lead_whatsapp_route': 'norte', // 'norte' o 'sur' segun el split
  'lead_province': 'cantabria'
});
```

### Evento 5: Conversión Secundaria - Llamada Directa (`lead_call`)
Se dispara cuando el usuario pulsa en el botón de llamar por teléfono.
* **Propósito:** Conversión telefónica.
```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'event': 'lead_call',
  'lead_source': 'calculator_result' // 'header', 'footer', 'calculator_result'
});
```

### Evento 6: Carga de Landing Geográfica (`page_view_geo`)
Se inyecta en la cabecera de las 72 subcarpetas de provincia.
* **Propósito:** Permite segmentar el tráfico orgánico por provincias en los reportes de GA4 y medir qué zonas geográficas son más rentables.
```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'page_geo_province': 'cantabria',
  'page_geo_city': 'santander',
  'page_silo': 'abogados' // 'abogados' o 'clinicas'
});
```

---

## 3. Estrategia de Mejoras en Conversión en sGTM (Google Ads y Facebook API)

Una vez los datos lleguen a tu servidor sGTM (`sst.infoaccidentes.com`), configuraremos:
1. **Google Ads Conversions (con Enhanced Conversions):** Envío directo de eventos de conversión al servidor de Google Ads. Al usar sGTM, la cookie de clic de Google Ads (`gclid`) no se pierde en Safari, mejorando la atribución de leads un 15-20%.
2. **Meta Conversions API (CAPI):** Envío simultáneo de los clics de WhatsApp y llamadas directamente al servidor de Meta. Al unificarlo con el Pixel del lado cliente, aumentamos el Event Quality Score mejorando el rendimiento de los anuncios de retargeting de lesionados.
3. **Control de Privacidad (Consensuado):** Configurar triggers que respeten la política de consentimiento de cookies estricta en España, enviando hits anonimizados en caso de rechazo del banner de cookies (Consent Mode V2).
