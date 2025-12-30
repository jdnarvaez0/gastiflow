<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <h1><i class="fas fa-wallet"></i> Gastiflow</h1>
                <p>Inicia sesión para continuar</p>
            </div>
            
            <form @submit.prevent="handleLogin" class="auth-form">
                <div class="form-group">
                    <label for="username">
                        <i class="fas fa-user"></i> Usuario
                    </label>
                    <input 
                        type="text" 
                        id="username" 
                        v-model="username" 
                        placeholder="Tu nombre de usuario"
                        required
                        :disabled="isLoading"
                    />
                </div>
                
                <div class="form-group">
                    <label for="password">
                        <i class="fas fa-lock"></i> Contraseña
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        v-model="password" 
                        placeholder="Tu contraseña"
                        required
                        :disabled="isLoading"
                    />
                </div>
                
                <div v-if="error" class="error-message">
                    <i class="fas fa-exclamation-circle"></i> {{ error }}
                </div>
                
                <button type="submit" class="btn-primary" :disabled="isLoading">
                    <i class="fas fa-sign-in-alt"></i>
                    {{ isLoading ? 'Cargando...' : 'Iniciar Sesión' }}
                </button>
            </form>
            
            <div class="auth-footer">
                <p>¿No tienes cuenta? <NuxtLink to="/register">Regístrate aquí</NuxtLink></p>
                <p style="margin-top: 0.75rem;"><NuxtLink to="/"><i class="fas fa-arrow-left"></i> Volver a la página principal</NuxtLink></p>
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

<style scoped>
.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    padding: 2rem;
}

.auth-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 2.5rem;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border-color);
}

.auth-header {
    text-align: center;
    margin-bottom: 2rem;
}

.auth-header h1 {
    font-size: 2rem;
    color: var(--accent-primary);
    margin-bottom: 0.5rem;
}

.auth-header h1 i {
    margin-right: 0.5rem;
}

.auth-header p {
    color: var(--text-secondary);
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-group label {
    color: var(--text-secondary);
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.form-group input {
    padding: 0.875rem 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus {
    outline: none;
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.2);
}

.form-group input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.error-message {
    padding: 0.75rem 1rem;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    color: #f87171;
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-primary {
    padding: 1rem;
    border-radius: 8px;
    border: none;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    color: white;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(147, 51, 234, 0.4);
}

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.auth-footer {
    text-align: center;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-color);
}

.auth-footer p {
    color: var(--text-secondary);
}

.auth-footer a {
    color: var(--accent-primary);
    text-decoration: none;
    font-weight: 500;
}

.auth-footer a:hover {
    text-decoration: underline;
}
</style>
