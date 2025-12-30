<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <h1><i class="fas fa-wallet"></i> Gastiflow</h1>
                <p>Crea tu cuenta gratis</p>
            </div>
            
            <form v-if="!showVerificationMessage" @submit.prevent="handleRegister" class="auth-form">
                <div class="form-group">
                    <label for="fullName">
                        <i class="fas fa-id-card"></i> Nombre completo
                    </label>
                    <input 
                        type="text" 
                        id="fullName" 
                        v-model="fullName" 
                        placeholder="Tu nombre y apellido"
                        :disabled="isLoading"
                    />
                </div>
                
                <div class="form-group">
                    <label for="username">
                        <i class="fas fa-user"></i> Usuario (para iniciar sesión)
                    </label>
                    <input 
                        type="text" 
                        id="username" 
                        v-model="username" 
                        placeholder="Elige un nombre de usuario"
                        required
                        minlength="3"
                        :disabled="isLoading"
                    />
                    <small style="color: var(--text-secondary); font-size: 0.75rem;">
                        Este será tu usuario para iniciar sesión
                    </small>
                </div>
                
                <div class="form-group">
                    <label for="email">
                        <i class="fas fa-envelope"></i> Email
                    </label>
                    <input 
                        type="email" 
                        id="email" 
                        v-model="email" 
                        placeholder="tu@email.com"
                        :disabled="isLoading"
                        required
                    />
                    <small style="color: var(--text-secondary); font-size: 0.75rem;">
                        Recibirás un link de verificación en tu email
                    </small>
                </div>
                
                <div class="form-group">
                    <label for="password">
                        <i class="fas fa-lock"></i> Contraseña
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        v-model="password" 
                        placeholder="Mínimo 6 caracteres"
                        required
                        minlength="6"
                        :disabled="isLoading"
                    />
                </div>
                
                <div class="form-group">
                    <label for="confirmPassword">
                        <i class="fas fa-lock"></i> Confirmar contraseña
                    </label>
                    <input 
                        type="password" 
                        id="confirmPassword" 
                        v-model="confirmPassword" 
                        placeholder="Repite tu contraseña"
                        required
                        :disabled="isLoading"
                    />
                </div>
                
                <div v-if="error || localError" class="error-message">
                    <i class="fas fa-exclamation-circle"></i> {{ localError || error }}
                </div>
                
                <button type="submit" class="btn-primary" :disabled="isLoading">
                    <i class="fas fa-user-plus"></i>
                    {{ isLoading ? 'Creando cuenta...' : 'Crear Cuenta' }}
                </button>
            </form>

            <!-- Email Verification Message -->
            <div v-else class="verification-message">
                <div class="success-icon">
                    <i class="fas fa-envelope-circle-check"></i>
                </div>
                <h2>¡Cuenta creada exitosamente!</h2>
                <p v-if="registeredEmail">
                    Te hemos enviado un email de verificación a <strong>{{ registeredEmail }}</strong>
                </p>
                <p v-else>
                    Tu cuenta ha sido creada. Puedes comenzar a usar Gastiflow ahora.
                </p>
                
                <div v-if="registeredEmail" class="info-box">
                    <i class="fas fa-info-circle"></i>
                    <span>Revisa tu bandeja de entrada y haz click en el link de verificación para activar tu cuenta.</span>
                </div>

                <div class="button-group">
                    <button @click="router.push('/')" class="btn-primary">
                        <i class="fas fa-home"></i> Ir al Dashboard
                    </button>
                    <button v-if="registeredEmail" @click="handleResendVerification" class="btn-secondary" :disabled="isResending">
                        <i class="fas fa-paper-plane"></i>
                        {{ isResending ? 'Reenviando...' : 'Reenviar email' }}
                    </button>
                </div>
            </div>
            
            <div class="auth-footer">
                <p>¿Ya tienes cuenta? <NuxtLink to="/login">Inicia sesión</NuxtLink></p>
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
const { register, resendVerification, isLoading, error, isAuthenticated } = useAuth()

const fullName = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const localError = ref<string | null>(null)
const showVerificationMessage = ref(false)
const registeredEmail = ref<string | null>(null)
const isResending = ref(false)

// Redirect if already authenticated
onMounted(() => {
    if (isAuthenticated.value) {
        router.push('/')
    }
})

const handleRegister = async () => {
    localError.value = null
    
    if (password.value !== confirmPassword.value) {
        localError.value = 'Las contraseñas no coinciden'
        return
    }
    
    const success = await register({
        username: username.value,
        password: password.value,
        email: email.value || undefined,
        full_name: fullName.value || undefined
    })
    
    if (success) {
        // Show verification message if email was provided
        if (email.value) {
            showVerificationMessage.value = true
            registeredEmail.value = email.value
        } else {
            // No email, go directly to dashboard
            router.push('/')
        }
    }
}

const handleResendVerification = async () => {
    isResending.value = true
    const success = await resendVerification()
    isResending.value = false
    
    if (success) {
        alert('Email de verificación reenviado exitosamente')
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
    gap: 1.25rem;
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

.verification-message {
    text-align: center;
    padding: 1rem 0;
}

.success-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto 1.5rem;
    background: linear-gradient(135deg, #10b981, #059669);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: white;
}

.verification-message h2 {
    color: var(--text-primary);
    margin-bottom: 1rem;
    font-size: 1.5rem;
}

.verification-message p {
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}

.info-box {
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
    padding: 1rem;
    margin: 1.5rem 0;
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    text-align: left;
}

.info-box i {
    color: #3b82f6;
    margin-top: 0.125rem;
}

.info-box span {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.button-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 1.5rem;
}

.btn-secondary {
    padding: 0.875rem 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.btn-secondary:hover:not(:disabled) {
    background: var(--bg-card);
    border-color: var(--accent-primary);
}

.btn-secondary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

</style>
