<template>
    <div class="min-h-screen flex items-center justify-center p-8">
        <div class="bg-landing-card rounded-2xl p-10 w-full max-w-md shadow-2xl border border-gray-700">
            <div class="text-center mb-8">
                <div class="flex items-center justify-center gap-3 mb-4">
                    <i class="fas fa-wallet text-3xl bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent"></i>
                    <span class="text-3xl font-bold bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">Gastiflow</span>
                </div>
                <p class="text-gray-400">{{ $t('auth.register.subtitle') }}</p>
            </div>
            
            <form v-if="!showVerificationMessage" @submit.prevent="handleRegister" class="flex flex-col gap-5">
                <div class="flex flex-col gap-2">
                    <label for="fullName" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-id-card"></i> {{ $t('auth.register.fullName') }}
                    </label>
                    <input 
                        type="text" 
                        id="fullName" 
                        v-model="fullName" 
                        :placeholder="$t('auth.register.fullNamePlaceholder')"
                        :disabled="isLoading"
                        class="px-4 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                    />
                </div>
                
                <div class="flex flex-col gap-2">
                    <label for="username" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-user"></i> {{ $t('auth.register.username') }}
                    </label>
                    <input 
                        type="text" 
                        id="username" 
                        v-model="username" 
                        :placeholder="$t('auth.register.usernamePlaceholder')"
                        required
                        minlength="3"
                        :disabled="isLoading"
                        class="px-4 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                    />
                    <small class="text-gray-500 text-xs">{{ $t('auth.register.usernameHint') }}</small>
                </div>
                
                <div class="flex flex-col gap-2">
                    <label for="email" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-envelope"></i> {{ $t('auth.register.email') }}
                    </label>
                    <input 
                        type="email" 
                        id="email" 
                        v-model="email" 
                        :placeholder="$t('auth.register.emailPlaceholder')"
                        :disabled="isLoading"
                        required
                        class="px-4 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                    />
                    <small class="text-gray-500 text-xs">{{ $t('auth.register.emailHint') }}</small>
                </div>
                
                <div class="flex flex-col gap-2">
                    <label for="password" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-lock"></i> {{ $t('auth.register.password') }}
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        v-model="password" 
                        :placeholder="$t('auth.register.passwordPlaceholder')"
                        required
                        minlength="6"
                        :disabled="isLoading"
                        class="px-4 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                    />
                </div>
                
                <div class="flex flex-col gap-2">
                    <label for="confirmPassword" class="text-gray-400 text-sm flex items-center gap-2">
                        <i class="fas fa-lock"></i> {{ $t('auth.register.confirmPassword') }}
                    </label>
                    <input 
                        type="password" 
                        id="confirmPassword" 
                        v-model="confirmPassword" 
                        :placeholder="$t('auth.register.confirmPasswordPlaceholder')"
                        required
                        :disabled="isLoading"
                        class="px-4 py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
                    />
                </div>
                
                <div v-if="error || localError" class="flex items-center gap-2 px-4 py-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                    <i class="fas fa-exclamation-circle"></i> {{ localError || error }}
                </div>
                
                <button 
                    type="submit" 
                    class="py-4 rounded-lg bg-gradient-to-r from-accent to-accent-light text-white font-semibold flex items-center justify-center gap-2 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-accent/40 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0 transition-all"
                    :disabled="isLoading"
                >
                    <i class="fas fa-user-plus"></i>
                    {{ isLoading ? $t('auth.register.submitting') : $t('auth.register.submit') }}
                </button>
            </form>

            <!-- Email Verification Message -->
            <div v-else class="text-center py-4">
                <div class="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center text-3xl text-white">
                    <i class="fas fa-envelope-circle-check"></i>
                </div>
                <h2 class="text-xl font-bold text-white mb-4">{{ $t('auth.register.success.title') }}</h2>
                <p v-if="registeredEmail" class="text-gray-400 mb-6">
                    {{ $t('auth.register.success.messageWithEmail') }} <strong class="text-white">{{ registeredEmail }}</strong>
                </p>
                <p v-else class="text-gray-400 mb-6">
                    {{ $t('auth.register.success.messageNoEmail') }}
                </p>
                
                <div v-if="registeredEmail" class="flex items-start gap-3 px-4 py-3 bg-blue-500/10 border border-blue-500/30 rounded-lg text-left mb-6">
                    <i class="fas fa-info-circle text-blue-400 mt-0.5"></i>
                    <span class="text-gray-400 text-sm">{{ $t('auth.register.success.verificationHint') }}</span>
                </div>

                <div class="flex flex-col gap-3">
                    <button @click="router.push('/')" class="py-3 rounded-lg bg-gradient-to-r from-accent to-accent-light text-white font-semibold flex items-center justify-center gap-2 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-accent/40 transition-all">
                        <i class="fas fa-home"></i> {{ $t('auth.register.success.goToDashboard') }}
                    </button>
                    <button v-if="registeredEmail" @click="handleResendVerification" class="py-3 rounded-lg border border-gray-600 bg-landing-secondary text-white font-medium flex items-center justify-center gap-2 hover:bg-landing-card hover:border-accent disabled:opacity-60 disabled:cursor-not-allowed transition-all" :disabled="isResending">
                        <i class="fas fa-paper-plane"></i>
                        {{ isResending ? $t('auth.register.success.resending') : $t('auth.register.success.resendEmail') }}
                    </button>
                </div>
            </div>
            
            <div class="text-center mt-6 pt-6 border-t border-gray-700">
                <p class="text-gray-400">
                    {{ $t('auth.register.hasAccount') }} 
                    <NuxtLink to="/login" class="text-accent font-medium hover:underline">{{ $t('auth.register.login') }}</NuxtLink>
                </p>
                <p class="mt-3">
                    <NuxtLink to="/" class="text-gray-400 hover:text-accent transition-colors">
                        <i class="fas fa-arrow-left"></i> {{ $t('auth.login.backToHome') }}
                    </NuxtLink>
                </p>
            </div>        </div>
    </div>
</template>

<script setup lang="ts">
// Use the public layout (no sidebar)
definePageMeta({
    layout: 'public'
})

const router = useRouter()
const { t } = useI18n()
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
        localError.value = t('auth.register.errors.passwordMismatch')
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
        alert(t('auth.register.success.resendSuccess'))
    }
}
</script>
