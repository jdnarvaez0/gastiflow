<template>
  <div class="flex min-h-screen w-full overflow-x-hidden">
    <!-- Desktop Sidebar (hidden on mobile) -->
    <nav class="hidden lg:flex fixed top-0 left-0 h-screen w-56 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 px-3 py-4 flex-col z-50">
      <div class="flex items-center gap-2 mb-4 px-2">
        <i class="fas fa-wallet text-xl text-primary"></i>
        <span class="text-lg font-bold text-primary">Gastiflow</span>
      </div>
      
      <ul class="flex-1 space-y-1">
        <li>
          <NuxtLink 
            to="/dashboard" 
            active-class="!bg-primary !text-white" 
            class="flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors"
          >
            <i class="fa-solid fa-chart-pie"></i> {{ $t('nav.dashboard') }}
          </NuxtLink>
        </li>
        <li>
          <NuxtLink 
            to="/movimientos" 
            active-class="!bg-primary !text-white" 
            class="flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors"
          >
            <i class="fa-solid fa-list"></i> {{ $t('nav.movements') }}
          </NuxtLink>
        </li>
        <li>
          <a href="#" class="flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
            <i class="fa-solid fa-chart-line"></i> {{ $t('nav.reports') }}
          </a>
        </li>
        <li>
          <a href="#" class="flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
            <i class="fa-solid fa-credit-card"></i> {{ $t('nav.accounts') }}
          </a>
        </li>
        <li>
          <a href="#" class="flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
            <i class="fa-solid fa-tags"></i> {{ $t('nav.categories') }}
          </a>
        </li>
      </ul>
      
      <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
        <ul class="space-y-1">
          <li v-if="isAuthenticated">
            <NuxtLink 
              to="/settings" 
              active-class="!bg-primary !text-white" 
              class="flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors"
            >
              <i class="fa-solid fa-gear"></i> {{ $t('nav.settings') }}
            </NuxtLink>
          </li>
          <li v-if="isAuthenticated">
            <a 
              href="#" 
              @click.prevent="handleLogout" 
              class="flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-red-500 hover:text-white text-sm transition-colors"
            >
              <i class="fa-solid fa-right-from-bracket"></i> {{ $t('nav.logout') }}
            </a>
          </li>
          <li v-if="!isAuthenticated">
            <NuxtLink 
              to="/login" 
              class="flex items-center gap-2 px-3 py-2.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors"
            >
              <i class="fa-solid fa-sign-in-alt"></i> {{ $t('auth.login.submit') }}
            </NuxtLink>
          </li>
        </ul>
        <div v-if="isAuthenticated && user" class="flex items-center gap-2 px-3 py-3 text-gray-500 dark:text-gray-400 text-sm border-t border-gray-200 dark:border-gray-700 mt-2">
          <i class="fa-solid fa-user-circle text-xl text-primary"></i>
          <span class="truncate">{{ user.username }}</span>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1 lg:ml-56 p-4 sm:p-6 lg:p-8 pb-24 lg:pb-8 bg-gray-100 dark:bg-gray-900 min-h-screen w-full max-w-full overflow-x-hidden">
      <div class="w-full max-w-full">
        <slot />
      </div>
    </main>

    <!-- Add Transaction Modal (accessible from bottom nav) -->
    <AddTransactionModal :is-open="showAddModal" @close="showAddModal = false" @saved="handleTransactionSaved" />

    <!-- Mobile Bottom Navigation Bar -->
    <nav class="lg:hidden fixed bottom-0 left-0 right-0 z-50 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 shadow-[0_-4px_20px_rgba(0,0,0,0.1)] dark:shadow-[0_-4px_20px_rgba(0,0,0,0.3)]">
      <div class="flex items-center justify-around px-2 py-1 safe-area-bottom">
        <!-- Dashboard -->
        <NuxtLink 
          to="/dashboard" 
          class="flex flex-col items-center justify-center py-2 px-3 rounded-xl transition-all group"
          :class="isActiveRoute('/dashboard') ? 'text-primary' : 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300'"
        >
          <div 
            class="w-10 h-10 flex items-center justify-center rounded-xl transition-all"
            :class="isActiveRoute('/dashboard') ? 'bg-primary/10' : 'group-hover:bg-gray-100 dark:group-hover:bg-gray-700'"
          >
            <i class="fa-solid fa-chart-pie text-lg"></i>
          </div>
          <span class="text-[10px] mt-1 font-medium">{{ $t('nav.dashboard') }}</span>
        </NuxtLink>

        <!-- Movements -->
        <NuxtLink 
          to="/movimientos" 
          class="flex flex-col items-center justify-center py-2 px-3 rounded-xl transition-all group"
          :class="isActiveRoute('/movimientos') ? 'text-primary' : 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300'"
        >
          <div 
            class="w-10 h-10 flex items-center justify-center rounded-xl transition-all"
            :class="isActiveRoute('/movimientos') ? 'bg-primary/10' : 'group-hover:bg-gray-100 dark:group-hover:bg-gray-700'"
          >
            <i class="fa-solid fa-list text-lg"></i>
          </div>
          <span class="text-[10px] mt-1 font-medium">{{ $t('nav.movements') }}</span>
        </NuxtLink>

        <!-- Add Button (Center - Floating Style) -->
        <button 
          @click="showAddModal = true"
          class="flex items-center justify-center w-14 h-14 -mt-6 rounded-full bg-gradient-to-br from-primary to-primary-dark text-white shadow-lg shadow-primary/40 hover:shadow-xl hover:shadow-primary/50 hover:scale-105 active:scale-95 transition-all"
        >
          <i class="fa-solid fa-plus text-xl"></i>
        </button>

        <!-- Reports -->
        <a 
          href="#" 
          class="flex flex-col items-center justify-center py-2 px-3 rounded-xl transition-all group text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <div class="w-10 h-10 flex items-center justify-center rounded-xl transition-all group-hover:bg-gray-100 dark:group-hover:bg-gray-700">
            <i class="fa-solid fa-chart-line text-lg"></i>
          </div>
          <span class="text-[10px] mt-1 font-medium">{{ $t('nav.reports') }}</span>
        </a>

        <!-- Settings -->
        <NuxtLink 
          to="/settings" 
          class="flex flex-col items-center justify-center py-2 px-3 rounded-xl transition-all group"
          :class="isActiveRoute('/settings') ? 'text-primary' : 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300'"
        >
          <div 
            class="w-10 h-10 flex items-center justify-center rounded-xl transition-all"
            :class="isActiveRoute('/settings') ? 'bg-primary/10' : 'group-hover:bg-gray-100 dark:group-hover:bg-gray-700'"
          >
            <i class="fa-solid fa-gear text-lg"></i>
          </div>
          <span class="text-[10px] mt-1 font-medium">{{ $t('nav.settings') }}</span>
        </NuxtLink>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import AddTransactionModal from '~/components/AddTransactionModal.vue'

const router = useRouter()
const route = useRoute()
const { setLocale } = useI18n()
const { user, isAuthenticated, logout, init } = useAuth()

// Modal state
const showAddModal = ref(false)

// Handle transaction saved - emit event or refresh
const handleTransactionSaved = () => {
  // Optionally trigger a refresh of the current page data
  window.dispatchEvent(new CustomEvent('transaction-saved'))
}

// Check if route is active
const isActiveRoute = (path: string) => {
  return route.path === path || route.path.startsWith(path + '/')
}

onMounted(async () => {
  await init()
  
  // Set language from user preference or localStorage
  if (user.value?.language) {
    setLocale(user.value.language as 'es' | 'en')
    localStorage.setItem('gastiflow_locale', user.value.language)
  } else {
    const savedLocale = localStorage.getItem('gastiflow_locale')
    if (savedLocale) {
      setLocale(savedLocale as 'es' | 'en')
    }
  }
})

// Watch for user changes to update language
watch(() => user.value?.language, (newLang) => {
  if (newLang) {
    setLocale(newLang as 'es' | 'en')
    localStorage.setItem('gastiflow_locale', newLang)
  }
})

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>

<style scoped>
/* Safe area for devices with home indicator (iPhone X+) */
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
</style>
