<template>
  <button 
    @click="toggleLocale" 
    class="flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/20 hover:border-accent/50 hover:bg-white/5 transition-all group"
    :title="$t('settings.preferences.language')"
  >
    <div class="flex items-center justify-center w-6 h-6 rounded-full bg-white/5 text-[10px] font-bold group-hover:bg-accent/20 group-hover:text-accent transition-colors">
      {{ nextLocale.toUpperCase() }}
    </div>
    <span class="text-xs font-semibold tracking-wider text-gray-300 group-hover:text-white uppercase">
      {{ locale }}
    </span>
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
