// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxt/ui', '@nuxtjs/i18n'],
  css: ['~/assets/css/style.css'],

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

  app: {
    head: {
      title: 'Gastiflow',
      link: [
        { rel: 'icon', type: 'image/png', href: '/favicon.png' },
        { rel: 'apple-touch-icon', href: '/icon.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;700&display=swap' },
        { rel: 'stylesheet', href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css' }
      ],
      script: [
        { src: 'https://cdn.jsdelivr.net/npm/chart.js' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiUrl: process.env.NUXT_API_URL || 'http://localhost:8000',
      telegramBotUsername: process.env.NUXT_TELEGRAM_BOT_USERNAME || 'gastiflow_dev_bot'
    }
  },

  nitro: {
    routeRules: {
      // Backend Proxies - Granular to avoid catching /api/_nuxt_icon
      '/api/register': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/register' } },
      '/api/login': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/login' } },
      '/api/me': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/me' } },
      '/api/refresh': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/refresh' } },
      '/api/logout': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/logout' } },
      '/api/settings': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/settings' } },
      '/api/verify-email': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/verify-email' } },
      '/api/resend-verification': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/resend-verification' } },
      '/api/email-status': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/email-status' } },
      '/api/profile-picture': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/profile-picture' } },
      '/api/expenses': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/expenses' } },
      '/api/expenses/**': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/expenses/**' } },
      '/api/dashboard': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/dashboard' } },
      '/api/health': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/health' } },
      '/api/telegram/**': { proxy: { to: (process.env.NUXT_API_URL || 'http://localhost:8000') + '/api/telegram/**' } },

      // Icon Cache
      '/api/_nuxt_icon/**': { cache: { maxAge: 1728000 } }
    }
  }
})