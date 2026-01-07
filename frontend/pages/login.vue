<template>
    <div class="min-h-screen flex items-center justify-center p-8">
        <div class="bg-landing-card rounded-2xl p-10 w-full max-w-md shadow-2xl border border-gray-700">
            <div class="text-center mb-8">
                <h1 class="text-3xl font-bold text-accent mb-2">
                    <i class="fas fa-wallet mr-2"></i>Gastiflow
                </h1>
                <p class="text-gray-400">Inicia sesión para continuar</p>
            </div>
            
            <form @submit.prevent="handleLogin" class="flex flex-col gap-6">
                <div class="flex flex-col gap-2">
                    <label for="username" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-user"></i> Usuario
                    </label>
                    <input 
                        type="text" 
                        id="username" 
                        v-model="username" 
                        placeholder="Tu nombre de usuario"
                        required
                        :disabled="isLoading"
                        class="px-4 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                    />
                </div>
                
                <div class="flex flex-col gap-2">
                    <label for="password" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-lock"></i> Contraseña
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        v-model="password" 
                        placeholder="Tu contraseña"
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
                    {{ isLoading ? 'Cargando...' : 'Iniciar Sesión' }}
                </button>
            </form>
            
            <div class="text-center mt-6 pt-6 border-t border-gray-700">
                <p class="text-gray-400">
                    ¿No tienes cuenta? 
                    <NuxtLink to="/register" class="text-accent font-medium hover:underline">Regístrate aquí</NuxtLink>
                </p>
                <p class="mt-3">
                    <NuxtLink to="/" class="text-gray-400 hover:text-accent transition-colors">
                        <i class="fas fa-arrow-left"></i> Volver a la página principal
                    </NuxtLink>
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
