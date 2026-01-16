function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

// Add event listeners if needed when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu button event listener
    const mobileMenuBtn = document.querySelector('button[onclick="toggleMobileMenu()"]');
    if (mobileMenuBtn) {
        // Just ensuring it works if inline onclick is removed later, but currently inline handles it.
    }

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
