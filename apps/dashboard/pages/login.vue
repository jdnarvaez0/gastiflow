<template>
    <div class="min-h-screen flex items-center justify-center p-8">
        <div class="bg-landing-card rounded-2xl p-10 w-full max-w-md shadow-2xl border border-gray-700">
            <div class="text-center mb-8">
                <div class="flex items-center justify-center gap-3 mb-4">
                    <i class="fas fa-wallet text-3xl bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent"></i>
                    <span class="text-3xl font-bold bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">Gastiflow</span>
                </div>
                <p class="text-gray-400">{{ $t('auth.login.subtitle') }}</p>
            </div>
            
            <form @submit.prevent="handleLogin" class="flex flex-col gap-6">
                <div class="flex flex-col gap-2">
                    <label for="username" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-user"></i> {{ $t('auth.login.username') }}
                    </label>
                    <input 
                        type="text" 
                        id="username" 
                        v-model="username" 
                        :placeholder="$t('auth.login.usernamePlaceholder')"
                        required
                        :disabled="isLoading"
                        class="px-4 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                    />
                </div>
                
                <div class="flex flex-col gap-2">
                    <label for="password" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-lock"></i> {{ $t('auth.login.password') }}
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        v-model="password" 
                        :placeholder="$t('auth.login.passwordPlaceholder')"
                        required
                        :disabled="isLoading"
                        class="px-4 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                    />
                </div>
                
                <div v-if="error" class="flex items-center gap-2 px-4 py-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                    <i class="fas fa-exclamation-circle"></i> {{ error }}
                </div>
                
                <button 
                    type="submit" 
                    class="py-4 rounded-lg bg-gradient-to-r from-accent to-accent-light text-white font-semibold flex items-center justify-center gap-2 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-accent/40 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0 transition-all"
                    :disabled="isLoading"
                >
                    <i class="fas fa-sign-in-alt"></i>
                    {{ isLoading ? $t('auth.login.loading') : $t('auth.login.submit') }}
                </button>
            </form>
            
            <div class="text-center mt-6 pt-6 border-t border-gray-700">
                <p class="text-gray-400">
                    {{ $t('auth.login.noAccount') }} 
                    <NuxtLink to="/register" class="text-accent font-medium hover:underline">{{ $t('auth.login.register') }}</NuxtLink>
                </p>
                <p class="mt-3">
                    <a :href="landingUrl" class="text-gray-400 hover:text-accent transition-colors">
                        <i class="fas fa-arrow-left"></i> {{ $t('auth.login.backToHome') }}
                    </a>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// Use the public layout (no sidebar)
definePageMeta({
    layout: 'public'
})

const router = useRouter()
const { login, isLoading, error, isAuthenticated } = useAuth()
const { public: { landingUrl } } = useRuntimeConfig()

const username = ref('')
const password = ref('')

// Redirect if already authenticated
onMounted(() => {
    if (isAuthenticated.value) {
        router.push('/dashboard')
    }
})

const handleLogin = async () => {
    const success = await login({ username: username.value, password: password.value })
    if (success) {
        router.push('/dashboard')
    }
}
</script>
