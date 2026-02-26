<template>
  <button 
    @click="toggleLocale" 
    class="flex items-center gap-1 px-2 py-1.5 rounded-lg hover:bg-white/10 dark:hover:bg-gray-700/50 transition-all group"
    :title="$t('settings.preferences.language')"
  >
    <span 
      class="text-xs font-bold tracking-wider uppercase transition-colors"
      :class="locale === 'en' ? 'text-accent' : 'text-gray-400 dark:text-gray-500'"
    >EN</span>
    <span class="text-gray-500 text-xs">/</span>
    <span 
      class="text-xs font-bold tracking-wider uppercase transition-colors"
      :class="locale === 'es' ? 'text-accent' : 'text-gray-400 dark:text-gray-500'"
    >ES</span>
  </button>
</template>

<script setup lang="ts">
const { locale, setLocale } = useI18n()

const nextLocale = computed(() => locale.value === 'es' ? 'en' : 'es')

const toggleLocale = () => {
  const newLocale = nextLocale.value
  setLocale(newLocale)
  // Persist in localStorage
  if (process.client) {
    localStorage.setItem('gastiflow_locale', newLocale)
  }
}

// Load saved locale on mount
onMounted(() => {
  if (process.client) {
    const savedLocale = localStorage.getItem('gastiflow_locale')
    if (savedLocale && savedLocale !== locale.value) {
      setLocale(savedLocale as 'es' | 'en')
    }
  }
})
</script>
