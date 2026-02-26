<template>
  <div class="min-h-screen flex items-center justify-center p-8">
    <div class="w-full max-w-lg">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="flex items-center justify-center gap-3">
            <i class="fas fa-wallet text-3xl bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent"></i>
            <span class="text-3xl font-bold bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">Gastiflow</span>
        </div>
      </div>

      <!-- Card -->
      <div class="bg-landing-card rounded-2xl p-12 shadow-2xl border border-gray-700">
        <!-- Loading State -->
        <div v-if="isVerifying" class="text-center">
          <div class="w-16 h-16 mx-auto mb-6 border-3 border-gray-700 border-t-accent rounded-full animate-spin"></div>
          <h2 class="text-2xl font-bold text-white mb-4">Verificando email...</h2>
          <p class="text-gray-400">Por favor espera un momento</p>
        </div>

        <!-- Success State -->
        <div v-else-if="verificationSuccess" class="text-center">
          <div class="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center text-4xl text-white">
            <i class="fas fa-check"></i>
          </div>
          <h2 class="text-2xl font-bold text-white mb-4">
            {{ alreadyVerified ? '¡Email ya verificado!' : '¡Email verificado!' }}
          </h2>
          <p class="text-gray-400 mb-8 leading-relaxed">
            {{ alreadyVerified 
              ? 'Tu email ya estaba verificado anteriormente.' 
              : 'Tu dirección de correo electrónico ha sido verificada exitosamente.' 
            }}
          </p>
          <NuxtLink to="/login" class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-gradient-to-r from-accent to-accent-light text-white font-semibold hover:-translate-y-0.5 hover:shadow-lg hover:shadow-accent/40 transition-all">
            <i class="fas fa-sign-in-alt"></i> Iniciar sesión
          </NuxtLink>
        </div>

        <!-- Error State -->
        <div v-else-if="verificationError" class="text-center">
          <div class="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center text-4xl text-white">
            <i class="fas fa-times"></i>
          </div>
          <h2 class="text-2xl font-bold text-white mb-4">Error de verificación</h2>
          <p class="text-gray-400 mb-8 leading-relaxed">{{ errorMessage }}</p>
          <div class="flex flex-col gap-3">
            <NuxtLink to="/login" class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-gradient-to-r from-accent to-accent-light text-white font-semibold hover:-translate-y-0.5 hover:shadow-lg hover:shadow-accent/40 transition-all">
              <i class="fas fa-sign-in-alt"></i> Iniciar sesión
            </NuxtLink>
            <NuxtLink to="/register" class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white font-medium hover:bg-landing-card hover:border-accent transition-all">
              <i class="fas fa-user-plus"></i> Registrarse
            </NuxtLink>
          </div>
        </div>

        <!-- No Token State -->
        <div v-else class="text-center">
          <div class="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-amber-500 to-amber-600 rounded-full flex items-center justify-center text-4xl text-white">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <h2 class="text-2xl font-bold text-white mb-4">Token no válido</h2>
          <p class="text-gray-400 mb-8 leading-relaxed">No se proporcionó un token de verificación válido.</p>
          <NuxtLink to="/" class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-gradient-to-r from-accent to-accent-light text-white font-semibold hover:-translate-y-0.5 hover:shadow-lg hover:shadow-accent/40 transition-all">
            <i class="fas fa-arrow-left"></i> Volver al inicio
          </NuxtLink>
        </div>
      </div>

      <!-- Footer -->
      <p class="text-center text-gray-500 mt-6 text-sm">
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
.border-3 {
    border-width: 3px;
}
</style>
