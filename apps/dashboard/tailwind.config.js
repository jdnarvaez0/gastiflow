/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    theme: {
        screens: {
            'xs': '480px',
            'sm': '640px',
            'md': '768px',
            'lg': '1024px',
            'xl': '1280px',
            '2xl': '1536px',
        },
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
                // Surface colors
                surface: {
                    light: '#f3f4f6',
                    card: '#ffffff',
                    cardDark: '#1f2937', // gray-800
                    dark: '#111827', // gray-900
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
