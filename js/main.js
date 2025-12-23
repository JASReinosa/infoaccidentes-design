function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

// Add event listeners if needed when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu button event listener could be added here to avoid inline onclick, 
    // but for now we'll stick to semantic function calls for simplicity in the HTML refactor.
});
