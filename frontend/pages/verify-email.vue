<template>
  <div class="verify-container">
    <div class="verify-card-wrapper">
      <!-- Card -->
      <div class="verify-card">
        <!-- Loading State -->
        <div v-if="isVerifying" class="verify-state">
          <div class="spinner"></div>
          <h2>Verificando email...</h2>
          <p>Por favor espera un momento</p>
        </div>

        <!-- Success State -->
        <div v-else-if="verificationSuccess" class="verify-state">
          <div class="icon-circle success">
            <i class="fas fa-check"></i>
          </div>
          <h2>
            {{ alreadyVerified ? '¡Email ya verificado!' : '¡Email verificado!' }}
          </h2>
          <p>
            {{ alreadyVerified 
              ? 'Tu email ya estaba verificado anteriormente.' 
              : 'Tu dirección de correo electrónico ha sido verificada exitosamente.' 
            }}
          </p>
          <NuxtLink to="/login" class="btn-primary">
            <i class="fas fa-sign-in-alt"></i> Iniciar sesión
          </NuxtLink>
        </div>

        <!-- Error State -->
        <div v-else-if="verificationError" class="verify-state">
          <div class="icon-circle error">
            <i class="fas fa-times"></i>
          </div>
          <h2>Error de verificación</h2>
          <p>{{ errorMessage }}</p>
          <div class="button-group">
            <NuxtLink to="/login" class="btn-primary">
              <i class="fas fa-sign-in-alt"></i> Iniciar sesión
            </NuxtLink>
            <NuxtLink to="/register" class="btn-secondary">
              <i class="fas fa-user-plus"></i> Registrarse
            </NuxtLink>
          </div>
        </div>

        <!-- No Token State -->
        <div v-else class="verify-state">
          <div class="icon-circle warning">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <h2>Token no válido</h2>
          <p>No se proporcionó un token de verificación válido.</p>
          <NuxtLink to="/" class="btn-primary">
            <i class="fas fa-arrow-left"></i> Volver al inicio
          </NuxtLink>
        </div>
      </div>

      <!-- Footer -->
      <p class="footer-text">
        © 2025 Gastiflow - Tu gestor de finanzas personales
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { verifyEmail } = useAuth()

const isVerifying = ref(false)
const verificationSuccess = ref(false)
const verificationError = ref(false)
const alreadyVerified = ref(false)
const errorMessage = ref('')

// Get token from query params
const token = computed(() => route.query.token as string)

// Verify email on mount
onMounted(async () => {
  if (!token.value) {
    return
  }

  isVerifying.value = true

  try {
    const result = await verifyEmail(token.value)
    
    if (result.success) {
      verificationSuccess.value = true
      alreadyVerified.value = result.alreadyVerified
    } else {
      verificationError.value = true
      errorMessage.value = 'El token de verificación es inválido o ha expirado.'
    }
  } catch (error) {
    verificationError.value = true
    errorMessage.value = 'Ocurrió un error al verificar tu email. Por favor intenta nuevamente.'
  } finally {
    isVerifying.value = false
  }
})
</script>

<style scoped>
.verify-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    padding: 2rem;
}

.verify-card-wrapper {
    width: 100%;
    max-width: 500px;
}

.verify-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 3rem 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border-color);
}

.verify-state {
    text-align: center;
}

.spinner {
    width: 64px;
    height: 64px;
    margin: 0 auto 1.5rem;
    border: 3px solid var(--border-color);
    border-top-color: var(--accent-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.icon-circle {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
}

.icon-circle.success {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
}

.icon-circle.error {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
}

.icon-circle.warning {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
}

.verify-state h2 {
    font-size: 1.75rem;
    color: var(--text-primary);
    margin-bottom: 1rem;
    font-weight: 700;
}

.verify-state p {
    color: var(--text-secondary);
    margin-bottom: 2rem;
    line-height: 1.6;
}

.btn-primary, .btn-secondary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(147, 51, 234, 0.4);
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--bg-card);
    border-color: var(--accent-primary);
}

.button-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.footer-text {
    text-align: center;
    color: var(--text-secondary);
    margin-top: 1.5rem;
    font-size: 0.875rem;
}
</style>
