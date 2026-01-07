/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                // Primary colors
                primary: {
                    DEFAULT: '#4f46e5',
                    light: '#818cf8',
                    dark: '#4338ca',
                },
                // Secondary/Accent colors
                accent: {
                    DEFAULT: '#9333ea',
                    light: '#a855f7',
                },
                // Status colors
                success: {
                    DEFAULT: '#4CE1B6',
                    light: '#D4FFE4',
                },
                danger: {
                    DEFAULT: '#FF754C',
                    light: '#FFEBE4',
                },
                // Surface colors (light mode)
                surface: {
                    light: '#f3f4f6',
                    card: '#ffffff',
                },
                // Landing page specific (always dark)
                landing: {
                    bg: '#0f0f1a',
                    card: '#1f1f35',
                    secondary: '#1a1a2e',
                },
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                display: ['Outfit', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
