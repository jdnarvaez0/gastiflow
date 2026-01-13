<template>
    <div class="min-h-screen flex flex-col bg-gradient-to-br from-landing-bg to-landing-secondary">
        <!-- Simple header for public pages -->
        <header class="fixed top-0 left-0 right-0 z-50 flex justify-between items-center px-8 py-5 bg-[rgba(17,17,27,0.85)] backdrop-blur-lg border-b border-white/5">
            <NuxtLink to="/" class="flex items-center gap-3 text-2xl font-bold text-accent hover:scale-[1.02] transition-transform no-underline">
                <i class="fas fa-wallet text-2xl bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent"></i>
                <span class="text-2xl font-bold bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">Gastiflow</span>
            </NuxtLink>
            <nav class="flex items-center gap-4">
                <LanguageSwitcher />
                <NuxtLink to="/login" class="px-5 py-2.5 text-gray-400 no-underline font-medium rounded-lg hover:text-white hover:bg-white/5 transition-all">
                    {{ $t('auth.login.submit') }}
                </NuxtLink>
                <NuxtLink to="/register" class="px-5 py-2.5 text-white no-underline font-medium rounded-lg bg-gradient-to-r from-accent to-accent-light hover:-translate-y-0.5 hover:shadow-lg hover:shadow-accent/40 transition-all">
                    {{ $t('auth.register.submit') }}
                </NuxtLink>
            </nav>
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

// If user is already authenticated and on landing, optionally redirect to dashboard
// This is commented out to allow authenticated users to view landing
// onMounted(() => {
//     if (isAuthenticated.value) {
//         navigateTo('/')
//     }
// })
</script>
