tailwind.config = {
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                "primary": "#0000FF",
                "primary-dark": "#0000cc",
                "primary-light": "#60a5fa",
                "background-light": "#f6f7f8",
                "background-dark": "#101922",
                "text-dark": "#0d141b",
                "text-muted": "#4b5563",
                "text-main": "#0d141b",
                "text-secondary": "#4c739a",
            },
            fontFamily: {
                "display": ["Public Sans", "sans-serif"],
                "body": ["Public Sans", "sans-serif"],
                "serif": ["Public Sans", "sans-serif"]
            },
            borderRadius: { "DEFAULT": "0.25rem", "lg": "0.5rem", "xl": "0.75rem", "2xl": "1rem", "full": "9999px" },
        },
    },
}