<template>
    <div class="min-h-screen flex flex-col bg-gradient-to-br from-landing-bg to-landing-secondary">
        <!-- Header for public pages - Responsive -->
        <header class="fixed top-0 left-0 right-0 z-50 px-4 sm:px-8 py-4 sm:py-5 bg-[rgba(17,17,27,0.92)] backdrop-blur-xl border-b border-white/5">
            <div class="flex justify-between items-center max-w-7xl mx-auto">
                <!-- Logo -->
                <a :href="landingUrl" class="flex items-center gap-2 sm:gap-3 text-xl sm:text-2xl font-bold text-accent hover:scale-[1.02] transition-transform no-underline">
                    <i class="fas fa-wallet text-xl sm:text-2xl bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent"></i>
                    <span class="text-xl sm:text-2xl font-bold bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">Gastiflow</span>
                </a>

                <!-- Desktop Navigation -->
                <nav class="hidden md:flex items-center gap-4">
                    <LanguageSwitcher />
                    <NuxtLink to="/login" class="px-5 py-2.5 text-gray-400 no-underline font-medium rounded-lg hover:text-white hover:bg-white/5 transition-all">
                        {{ $t('auth.login.submit') }}
                    </NuxtLink>
                    <NuxtLink to="/register" class="px-5 py-2.5 text-white no-underline font-medium rounded-lg bg-gradient-to-r from-accent to-accent-light hover:-translate-y-0.5 hover:shadow-lg hover:shadow-accent/40 transition-all">
                        {{ $t('auth.register.submit') }}
                    </NuxtLink>
                </nav>

                <!-- Mobile Menu Button -->
                <button 
                    @click="toggleMobileMenu"
                    class="md:hidden flex flex-col justify-center items-center w-10 h-10 rounded-lg bg-white/5 hover:bg-white/10 transition-all"
                    :aria-expanded="isMobileMenuOpen"
                    aria-label="Toggle menu"
                >
                    <span 
                        class="block w-5 h-0.5 bg-white rounded-full transition-all duration-300 ease-out"
                        :class="isMobileMenuOpen ? 'rotate-45 translate-y-1.5' : ''"
                    ></span>
                    <span 
                        class="block w-5 h-0.5 bg-white rounded-full mt-1 transition-all duration-300 ease-out"
                        :class="isMobileMenuOpen ? 'opacity-0 scale-0' : ''"
                    ></span>
                    <span 
                        class="block w-5 h-0.5 bg-white rounded-full mt-1 transition-all duration-300 ease-out"
                        :class="isMobileMenuOpen ? '-rotate-45 -translate-y-1.5' : ''"
                    ></span>
                </button>
            </div>

            <!-- Mobile Menu Dropdown -->
            <Transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="opacity-0 -translate-y-4 max-h-0"
                enter-to-class="opacity-100 translate-y-0 max-h-96"
                leave-active-class="transition-all duration-200 ease-in"
                leave-from-class="opacity-100 translate-y-0 max-h-96"
                leave-to-class="opacity-0 -translate-y-4 max-h-0"
            >
                <nav 
                    v-show="isMobileMenuOpen"
                    class="md:hidden mt-4 pt-4 border-t border-white/10 overflow-hidden"
                >
                    <div class="flex flex-col gap-3">
                        <!-- Language Switcher -->
                        <div class="flex justify-center py-2">
                            <LanguageSwitcher />
                        </div>
                        
                        <!-- Login Link -->
                        <NuxtLink 
                            to="/login" 
                            @click="closeMobileMenu"
                            class="flex items-center justify-center gap-2 px-5 py-3 text-gray-300 no-underline font-medium rounded-xl hover:text-white hover:bg-white/5 transition-all"
                        >
                            <i class="fas fa-sign-in-alt"></i>
                            {{ $t('auth.login.submit') }}
                        </NuxtLink>
                        
                        <!-- Register Link -->
                        <NuxtLink 
                            to="/register" 
                            @click="closeMobileMenu"
                            class="flex items-center justify-center gap-2 px-5 py-3 text-white no-underline font-semibold rounded-xl bg-gradient-to-r from-accent to-accent-light hover:shadow-lg hover:shadow-accent/40 transition-all"
                        >
                            <i class="fas fa-user-plus"></i>
                            {{ $t('auth.register.submit') }}
                        </NuxtLink>
                    </div>
                </nav>
            </Transition>
        </header>

        <!-- Main content -->
        <main class="flex-1 mt-20">
            <slot />
        </main>

        <!-- Footer -->
        <footer class="text-center py-8 text-gray-400 text-sm border-t border-gray-700">
            <p>&copy; 2025 Gastiflow.</p>
        </footer>
    </div>
</template>

<script setup lang="ts">
const { isAuthenticated } = useAuth()
const { public: { landingUrl } } = useRuntimeConfig()

// Mobile menu state
const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
    isMobileMenuOpen.value = false
}

// Close menu on route change
const route = useRoute()
watch(() => route.path, () => {
    closeMobileMenu()
})

// Close menu on escape key
onMounted(() => {
    const handleEscape = (e: KeyboardEvent) => {
        if (e.key === 'Escape' && isMobileMenuOpen.value) {
            closeMobileMenu()
        }
    }
    window.addEventListener('keydown', handleEscape)
    onUnmounted(() => {
        window.removeEventListener('keydown', handleEscape)
    })
})
</script>
