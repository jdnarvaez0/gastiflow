// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  
  modules: [
    '@nuxt/ui',
    '@nuxtjs/i18n'
  ],
  
  // Generar sitio estático (SSG) - Mejor para SEO y performance
  nitro: {
    preset: 'static',
    prerender: {
      routes: ['/']
    }
  },
  
  app: {
    head: {
      title: 'Gastiflow - Control de Gastos con IA',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { 
          name: 'description', 
          content: 'Gastiflow es tu asistente financiero personal. Controla tus gastos vía Telegram con inteligencia artificial. Gratis para siempre.' 
        },
        { name: 'theme-color', content: '#9333ea' },
        // Open Graph
        { property: 'og:title', content: 'Gastiflow - Control de Gastos con IA' },
        { property: 'og:description', content: 'Tu asistente financiero personal via Telegram' },
        { property: 'og:type', content: 'website' },
        { property: 'og:image', content: '/banner.png' },
        // Twitter
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'Gastiflow - Control de Gastos con IA' },
        { name: 'twitter:description', content: 'Tu asistente financiero personal via Telegram' },
        { name: 'twitter:image', content: '/banner.png' }
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/favicon.png' },
        { rel: 'apple-touch-icon', href: '/icon.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;700&display=swap' },
        { rel: 'stylesheet', href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css' }
      ]
    }
  },
  
  i18n: {
    defaultLocale: 'es',
    locales: [
      { code: 'es', name: 'Español', file: 'es.json' },
      { code: 'en', name: 'English', file: 'en.json' }
    ],
    lazy: false,
    langDir: 'locales',
    strategy: 'no_prefix',
    detectBrowserLanguage: false
  },
  
  css: ['~/assets/css/style.css'],
  
  colorMode: {
    preference: 'dark',
    fallback: 'dark'
  },
  
  compatibilityDate: '2026-02-26'
})
