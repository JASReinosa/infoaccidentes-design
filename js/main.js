function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

// Add event listeners if needed when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {


    // Update WhatsApp links to include current page URL
    const waLinks = document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"]');
    const currentUrl = window.location.href;

    waLinks.forEach(link => {
        try {
            const url = new URL(link.href);
            const params = new URLSearchParams(url.search);
            let text = params.get('text') || '';

            // Only append if not already present
            if (!text.includes(currentUrl)) {
                text += ` desde ${currentUrl}`;
                params.set('text', text);
                url.search = params.toString();
                link.href = url.toString();
            }
        } catch (e) {
            console.error('Error updating WhatsApp link:', e);
        }
    });
});

// Search Widget Functionality
let currentSearchMode = 'abogados'; // Default

function setSearchMode(mode) {
    currentSearchMode = mode;
    const btnAbogado = document.getElementById('btn-abogado');
    const btnClinica = document.getElementById('btn-clinica');
    const btnSearchText = document.getElementById('btn-search-text');
    const locationSelect = document.getElementById('search-location');

    if (mode === 'abogados') {
        // Activate Abogado
        btnAbogado.className = "flex items-center justify-center gap-2 py-3 px-4 rounded-md bg-white text-primary font-bold shadow-sm transition-all";
        // Deactivate Clinica
        btnClinica.className = "flex items-center justify-center gap-2 py-3 px-4 rounded-md text-muted hover:text-primary hover:bg-white/50 font-medium transition-all";
        btnSearchText.textContent = "Buscar Abogado";
        // locationSelect.placeholder = "Provincia del abogado..."; // Select doesn't use placeholder like input
    } else {
        // Activate Clinica
        btnClinica.className = "flex items-center justify-center gap-2 py-3 px-4 rounded-md bg-white text-primary font-bold shadow-sm transition-all";
        // Deactivate Abogado
        btnAbogado.className = "flex items-center justify-center gap-2 py-3 px-4 rounded-md text-muted hover:text-primary hover:bg-white/50 font-medium transition-all";
        btnSearchText.textContent = "Buscar Clínica";
    }
}

function performSearch() {
    const locationSelect = document.getElementById('search-location');
    const locationValue = locationSelect.value;

    if (!locationValue) {
        // Shake animation/alert for validation
        locationSelect.parentElement.classList.add('animate-shake');
        setTimeout(() => locationSelect.parentElement.classList.remove('animate-shake'), 500);
        locationSelect.focus();
        return;
    }

    // Determine path base
    const basePath = currentSearchMode === 'abogados' ? 'abogados-trafico' : 'clinicas-accidentes-trafico';

    // Redirect
    // Using relative path assuming we are at root index.html. 
    // To be safe for any depth if this widget is reused, absolute path is better but sticking to relative as requested structure implies root.
    // However, clean URLs usually end in slash.
    window.location.href = `${basePath}/${locationValue}/index.html`;
}
