<template>
    <div class="max-w-4xl mx-auto p-6">
        <div class="mb-8">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3 mb-2">
                <i class="fas fa-cog"></i> {{ $t('settings.title') }}
            </h1>
            <p class="text-gray-500 dark:text-gray-400">{{ $t('settings.subtitle') }}</p>
        </div>
        
        <div class="grid gap-6 md:grid-cols-2">
            <!-- Profile & Photo Card -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
                    <i class="fas fa-user"></i> {{ $t('settings.profile.title') }}
                </h2>
                
                <!-- Avatar Section -->
                <div class="flex flex-col items-center gap-4 p-6 bg-gray-50 dark:bg-gray-900 rounded-xl mb-6">
                    <UserAvatar 
                        :image-url="user?.profile_picture_url" 
                        :name="user?.full_name || user?.username"
                        :username="user?.username"
                        size="xl"
                    />
                    <div class="flex gap-2">
                        <label class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 font-medium hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer transition-colors flex items-center gap-2">
                            <i class="fas fa-camera"></i>
                            {{ user?.profile_picture_url ? $t('settings.profile.changePhoto') : $t('settings.profile.uploadPhoto') }}
                            <input 
                                type="file" 
                                accept="image/jpeg,image/png,image/gif,image/webp"
                                @change="handleFileUpload"
                                :disabled="isUploadingPhoto"
                                hidden
                            />
                        </label>
                        <button 
                            v-if="user?.profile_picture_url" 
                            @click="handleDeletePhoto" 
                            class="px-4 py-2 border border-red-300 dark:border-red-700 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors flex items-center gap-2"
                            :disabled="isUploadingPhoto"
                        >
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    <p class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
                        <i class="fas fa-info-circle"></i>
                        {{ $t('settings.profile.photoHint') }}
                    </p>
                </div>
                
                <!-- Profile Info -->
                <div class="space-y-3 mb-6">
                    <div class="flex justify-between">
                        <span class="text-gray-500 dark:text-gray-400 text-sm">{{ $t('settings.profile.username') }}:</span>
                        <span class="text-gray-900 dark:text-white font-medium">{{ user?.username }}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-500 dark:text-gray-400 text-sm">{{ $t('settings.profile.interactionsUsed') }}:</span>
                        <span class="text-gray-900 dark:text-white font-medium">{{ user?.interaction_count || 0 }}</span>
                    </div>
                </div>
                
                <!-- Full Name Form -->
                <form @submit.prevent="handleSaveFullName" class="space-y-4">
                    <div>
                        <label for="full_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ $t('settings.profile.fullName') }}</label>
                        <input 
                            type="text" 
                            id="full_name" 
                            v-model="fullName" 
                            placeholder="Ej: Juan Narvaez"
                            :disabled="isLoading"
                            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:opacity-60"
                        />
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-2 flex items-center gap-1">
                            <i class="fas fa-info-circle"></i>
                            {{ $t('settings.profile.fullNameHint') }}
                        </p>
                    </div>
                    <button type="submit" class="w-full py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2" :disabled="isLoading || !hasFullNameChanged">
                        <i class="fas fa-save"></i>
                        {{ isLoading ? $t('common.loading') : $t('settings.profile.saveName') }}
                    </button>
                </form>
            </div>
            
            <!-- Email Card -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
                    <i class="fas fa-envelope"></i> Email
                </h2>
                <div class="space-y-3 mb-6">
                    <div class="flex justify-between items-center flex-wrap gap-2">
                        <span class="text-gray-500 dark:text-gray-400 text-sm">Email actual:</span>
                        <span class="text-gray-900 dark:text-white font-medium flex items-center gap-2 flex-wrap">
                            {{ user?.email || 'No configurado' }}
                            <span v-if="user?.email" class="px-2 py-1 rounded-full text-xs font-medium" :class="user?.email_verified ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'">
                                <i :class="user?.email_verified ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
                                {{ user?.email_verified ? 'Verificado' : 'No verificado' }}
                            </span>
                        </span>
                    </div>
                </div>
                
                <!-- Resend Verification Button -->
                <div v-if="user?.email && !user?.email_verified" class="mb-6">
                    <button @click="handleResendVerification" class="w-full py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 font-medium hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2" :disabled="isResending">
                        <i class="fas fa-paper-plane"></i>
                        {{ isResending ? 'Reenviando...' : 'Reenviar verificación' }}
                    </button>
                </div>
                
                <!-- Change Email Form -->
                <form @submit.prevent="handleChangeEmail" class="space-y-4">
                    <div>
                        <label for="new_email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            {{ user?.email ? 'Cambiar email' : 'Agregar email' }}
                        </label>
                        <input 
                            type="email" 
                            id="new_email" 
                            v-model="newEmail" 
                            :placeholder="user?.email || 'tu@email.com'"
                            :disabled="isLoading"
                            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:opacity-60"
                        />
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-2 flex items-center gap-1">
                            <i class="fas fa-info-circle"></i>
                            {{ user?.email ? 'Recibirás verificación en la nueva dirección' : 'Recibirás un email de verificación' }}
                        </p>
                    </div>
                    
                    <button type="submit" class="w-full py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2" :disabled="isLoading || !newEmail || newEmail === user?.email">
                        <i class="fas fa-save"></i>
                        {{ isLoading ? 'Guardando...' : (user?.email ? 'Cambiar Email' : 'Agregar Email') }}
                    </button>
                </form>
            </div>
            
            <!-- API Key Card -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
                    <i class="fas fa-key"></i> API Key de Gemini
                </h2>
                <div class="px-4 py-3 rounded-lg mb-6 flex items-center gap-2" :class="user?.has_gemini_key ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'">
                    <i :class="user?.has_gemini_key ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
                    {{ user?.has_gemini_key ? 'API Key configurada' : 'Sin API Key' }}
                </div>
                
                <form @submit.prevent="saveApiKey" class="space-y-4">
                    <div>
                        <label for="gemini_key" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Nueva API Key</label>
                        <input 
                            type="password" 
                            id="gemini_key" 
                            v-model="geminiApiKey" 
                            placeholder="AIza..."
                            :disabled="isLoading"
                            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:opacity-60"
                        />
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-2 flex items-center gap-1">
                            <i class="fas fa-info-circle"></i>
                            Obtén tu API Key en 
                            <a href="https://aistudio.google.com/app/apikey" target="_blank" class="text-primary hover:underline">Google AI Studio</a>
                        </p>
                    </div>
                    
                    <button type="submit" class="w-full py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2" :disabled="isLoading || !geminiApiKey">
                        <i class="fas fa-save"></i>
                        {{ isLoading ? 'Guardando...' : 'Guardar API Key' }}
                    </button>
                </form>
            </div>
            
            <!-- Telegram Card -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
                    <i class="fab fa-telegram"></i> Telegram
                </h2>
                <div class="space-y-3 mb-6">
                    <div class="flex justify-between">
                        <span class="text-gray-500 dark:text-gray-400 text-sm">Estado:</span>
                        <span class="font-medium" :class="user?.telegram_id ? 'text-green-600 dark:text-green-400' : 'text-yellow-600 dark:text-yellow-400'">
                            {{ user?.telegram_id ? '✅ Vinculado' : '⚠️ No vinculado' }}
                        </span>
                    </div>
                    <div v-if="user?.telegram_id" class="flex justify-between">
                        <span class="text-gray-500 dark:text-gray-400 text-sm">Telegram ID:</span>
                        <span class="text-gray-900 dark:text-white font-medium">{{ user.telegram_id }}</span>
                    </div>
                </div>
                
                <!-- Link Code Generation -->
                <div v-if="!user?.telegram_id" class="space-y-4">
                    <button 
                        @click="handleGenerateLinkCode" 
                        class="w-full py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark disabled:opacity-50 transition-colors flex items-center justify-center gap-2" 
                        :disabled="isLoading || showLinkCode"
                    >
                        <i class="fas fa-qrcode"></i>
                        {{ isLoading ? 'Generando...' : 'Generar Código de Vinculación' }}
                    </button>
                    
                    <!-- Link Code Display -->
                    <div v-if="showLinkCode" class="space-y-4">
                        <div class="p-4 bg-gray-50 dark:bg-gray-900 rounded-xl text-center">
                            <div class="text-sm text-gray-500 dark:text-gray-400 mb-2">Tu código:</div>
                            <div class="text-3xl font-bold tracking-wider text-primary font-mono mb-2">{{ linkCode }}</div>
                            <div class="text-sm text-gray-500 dark:text-gray-400 flex items-center justify-center gap-2">
                                <i class="fas fa-clock"></i>
                                Expira en {{ formatTimeRemaining(linkCodeExpiry) }}
                            </div>
                        </div>
                        
                        <div class="p-4 bg-gray-50 dark:bg-gray-900 rounded-xl">
                            <h4 class="font-medium text-gray-900 dark:text-white flex items-center gap-2 mb-3">
                                <i class="fas fa-info-circle"></i> Instrucciones:
                            </h4>
                            <ol class="list-decimal ml-5 space-y-2 text-sm text-gray-500 dark:text-gray-400">
                                <li>Abre Telegram y busca el bot</li>
                                <li>Envía: <code class="px-2 py-1 bg-primary/10 text-primary rounded">/link {{ linkCode }}</code></li>
                                <li>Espera la confirmación</li>
                            </ol>
                            <a :href="telegramBotUrl" target="_blank" class="mt-4 inline-flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                                <i class="fab fa-telegram"></i> Abrir Bot
                            </a>
                        </div>
                        
                        <div v-if="isPolling" class="flex items-center justify-center gap-2 py-3 px-4 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg">
                            <i class="fas fa-spinner fa-spin"></i>
                            Esperando vinculación...
                        </div>
                    </div>
                </div>
                
                <!-- Already Linked -->
                <div v-else class="space-y-4">
                    <div class="flex items-center gap-3 py-3 px-4 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 rounded-lg">
                        <i class="fas fa-check-circle text-xl"></i>
                        <span>Tu Telegram está vinculado correctamente.</span>
                    </div>
                    <button 
                        @click="handleUnlinkTelegram" 
                        class="w-full py-2.5 border border-red-300 dark:border-red-700 text-red-600 dark:text-red-400 rounded-lg font-medium hover:bg-red-50 dark:hover:bg-red-900/20 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
                        :disabled="isLoading"
                    >
                        <i class="fas fa-unlink"></i>
                        {{ isLoading ? 'Desvinculando...' : 'Desvincular Telegram' }}
                    </button>
                </div>
            </div>
            
            <!-- Preferences Card -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm md:col-span-2">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
                    <i class="fas fa-sliders"></i> {{ $t('settings.preferences.title') }}
                </h2>
                
                <form @submit.prevent="handleSavePreferences" class="grid gap-6 md:grid-cols-3">
                    <!-- Currency -->
                    <div>
                        <label for="currency" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ $t('settings.preferences.currency') }}</label>
                        <select 
                            id="currency" 
                            v-model="selectedCurrency"
                            :disabled="isLoading"
                            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:opacity-60"
                        >
                            <option value="COP">🇨🇴 COP - Peso Colombiano</option>
                            <option value="USD">🇺🇸 USD - Dólar Americano</option>
                            <option value="EUR">🇪🇺 EUR - Euro</option>
                            <option value="ARS">🇦🇷 ARS - Peso Argentino</option>
                            <option value="MXN">🇲🇽 MXN - Peso Mexicano</option>
                        </select>
                    </div>
                    
                    <!-- Timezone -->
                    <div>
                        <label for="timezone" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ $t('settings.preferences.timezone') }}</label>
                        <select 
                            id="timezone" 
                            v-model="selectedTimezone"
                            :disabled="isLoading"
                            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:opacity-60"
                        >
                            <option value="America/Bogota">🇨🇴 Bogotá (GMT-5)</option>
                            <option value="America/Mexico_City">🇲🇽 Ciudad de México (GMT-6)</option>
                            <option value="America/Buenos_Aires">🇦🇷 Buenos Aires (GMT-3)</option>
                            <option value="America/Lima">🇵🇪 Lima (GMT-5)</option>
                            <option value="America/Santiago">🇨🇱 Santiago (GMT-4)</option>
                            <option value="America/New_York">🇺🇸 New York (GMT-5)</option>
                            <option value="Europe/Madrid">🇪🇸 Madrid (GMT+1)</option>
                        </select>
                    </div>
                    
                    <!-- Language -->
                    <div>
                        <label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{{ $t('settings.preferences.language') }}</label>
                        <select 
                            id="language" 
                            v-model="selectedLanguage"
                            :disabled="isLoading"
                            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:opacity-60"
                        >
                            <option value="es">🇪🇸 Español</option>
                            <option value="en">🇬🇧 English</option>
                        </select>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-2 flex items-center gap-1">
                            <i class="fas fa-info-circle"></i>
                            {{ $t('settings.preferences.languageHint') }}
                        </p>
                    </div>
                    
                    <div class="md:col-span-3">
                        <button type="submit" class="w-full py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2" :disabled="isLoading || !hasPreferencesChanged">
                            <i class="fas fa-save"></i>
                            {{ isLoading ? $t('common.loading') : $t('settings.preferences.save') }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Back Button -->
        <div class="mt-8 flex justify-between items-center">
            <NuxtLink to="/dashboard" class="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-primary dark:hover:text-primary transition-colors">
                <i class="fas fa-arrow-left"></i> Volver al Dashboard
            </NuxtLink>
            
            <button @click="handleLogout" class="flex items-center gap-2 text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 transition-colors">
                <i class="fas fa-sign-out-alt"></i> Cerrar Sesión
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
const router = useRouter()
const { setLocale  } = useI18n()
const { user, isLoading, error, updateSettings, logout, isAuthenticated, init, changeEmail, resendVerification, uploadProfilePicture, deleteProfilePicture, generateLinkCode, checkLinkStatus, unlinkTelegram, isLoggingOut } = useAuth()
const { success: notifySuccess, error: notifyError } = useNotification()

const geminiApiKey = ref('')
const newEmail = ref('')
const isResending = ref(false)
const fullName = ref('')
const isUploadingPhoto = ref(false)

// Telegram link code state
const linkCode = ref('')
const linkCodeExpiry = ref<Date | null>(null)
const showLinkCode = ref(false)
const isPolling = ref(false)
const pollingInterval = ref<NodeJS.Timeout | null>(null)
const timerInterval = ref<NodeJS.Timeout | null>(null)

// Preferences state
const selectedCurrency = ref('ARS')
const selectedTimezone = ref('America/Bogota')
const selectedLanguage = ref('es')

// Telegram bot URL
const config = useRuntimeConfig()
const telegramBotUrl = computed(() => {
    const botUsername = config.public.telegramBotUsername || 'GastiflowBot'
    return `https://t.me/${botUsername}`
})

// Initialize auth on mount
onMounted(async () => {
    await init()
    if (!isAuthenticated.value) {
        router.push('/login')
        return
    }
    if (user.value?.full_name) {
        fullName.value = user.value.full_name
    }
    // Initialize preferences from user data
    if (user.value?.preferred_currency) {
        selectedCurrency.value = user.value.preferred_currency
    }
    if (user.value?.timezone) {
        selectedTimezone.value = user.value.timezone
    }
    if (user.value?.language) {
        selectedLanguage.value = user.value.language
    }
})

// Cleanup intervals on unmount
onUnmounted(() => {
    stopPolling()
    stopTimer()
})

// Check if full name has changed
const hasFullNameChanged = computed(() => {
    return fullName.value !== (user.value?.full_name || '')
})

// Check if preferences have changed
const hasPreferencesChanged = computed(() => {
    return selectedCurrency.value !== (user.value?.preferred_currency || 'ARS') ||
           selectedTimezone.value !== (user.value?.timezone || 'America/Bogota') ||
           selectedLanguage.value !== (user.value?.language || 'es')
})

const saveApiKey = async () => {
    const success = await updateSettings({ gemini_api_key: geminiApiKey.value })
    if (success) {
        notifySuccess('Éxito', 'API Key guardada correctamente')
        geminiApiKey.value = ''
    } else if (error.value) {
        notifyError('Error', error.value)
    }
}

// Telegram Link Code Functions
const handleGenerateLinkCode = async () => {
    const response = await generateLinkCode()
    
    if (response) {
        linkCode.value = response.code
        linkCodeExpiry.value = new Date(response.expires_at)
        showLinkCode.value = true
        startPolling()
        startTimer()
    }
}

const startPolling = () => {
    isPolling.value = true
    pollingInterval.value = setInterval(async () => {
        const status = await checkLinkStatus()
        if (status?.linked) {
            notifySuccess('Éxito', '¡Telegram vinculado exitosamente!')
            stopPolling()
            stopTimer()
            showLinkCode.value = false
            linkCode.value = ''
        }
    }, 3000)
}

const stopPolling = () => {
    isPolling.value = false
    if (pollingInterval.value) {
        clearInterval(pollingInterval.value)
        pollingInterval.value = null
    }
}

const startTimer = () => {
    timerInterval.value = setInterval(() => {
        if (linkCodeExpiry.value && new Date() >= linkCodeExpiry.value) {
            stopTimer()
            stopPolling()
            showLinkCode.value = false
            notifyError('Error', 'El código ha expirado. Genera uno nuevo.')
        }
    }, 1000)
}

const stopTimer = () => {
    if (timerInterval.value) {
        clearInterval(timerInterval.value)
        timerInterval.value = null
    }
}

const formatTimeRemaining = (expiry: Date | null) => {
    if (!expiry) return '0:00'
    const now = new Date()
    const diff = expiry.getTime() - now.getTime()
    if (diff <= 0) return '0:00'
    const minutes = Math.floor(diff / 60000)
    const seconds = Math.floor((diff % 60000) / 1000)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

const handleChangeEmail = async () => {
    const success = await changeEmail(newEmail.value)
    if (success) {
        notifySuccess('Éxito', 'Email actualizado. Revisa tu bandeja de entrada.')
        newEmail.value = ''
    } else if (error.value) {
        toast.add({ title: 'Error', description: error.value, color: 'red' })
    }
}

const handleResendVerification = async () => {
    isResending.value = true
    const success = await resendVerification()
    isResending.value = false
    if (success) {
        notifySuccess('Éxito', 'Email de verificación reenviado')
    } else if (error.value) {
        toast.add({ title: 'Error', description: error.value, color: 'red' })
    }
}

const handleLogout = () => {
    logout()
    // No router.push needed - logout redirects to landing page
}

const handleSaveFullName = async () => {
    const success = await updateSettings({ full_name: fullName.value || null })
    if (success) {
        notifySuccess('Éxito', 'Nombre guardado correctamente')
    } else if (error.value) {
        toast.add({ title: 'Error', description: error.value, color: 'red' })
    }
}

const handleSavePreferences = async () => {
    const success = await updateSettings({
        preferred_currency: selectedCurrency.value,
        timezone: selectedTimezone.value,
        language: selectedLanguage.value
    })
    if (success) {
        // Change the app language
        setLocale(selectedLanguage.value)
        notifySuccess('Éxito', 'Preferencias guardadas correctamente')
    } else if (error.value) {
        toast.add({ title: 'Error', description: error.value, color: 'red' })
    }
}

const handleFileUpload = async (event: Event) => {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0]
    if (!file) return
    
    isUploadingPhoto.value = true
    const success = await uploadProfilePicture(file)
    isUploadingPhoto.value = false
    if (success) {
        notifySuccess('Éxito', 'Foto de perfil actualizada')
    } else if (error.value) {
        toast.add({ title: 'Error', description: error.value, color: 'red' })
    }
    target.value = ''
}

const handleDeletePhoto = async () => {
    isUploadingPhoto.value = true
    const success = await deleteProfilePicture()
    isUploadingPhoto.value = false
    if (success) {
        notifySuccess('Éxito', 'Foto de perfil eliminada')
    } else if (error.value) {
        toast.add({ title: 'Error', description: error.value, color: 'red' })
    }
}

const handleUnlinkTelegram = async () => {
    if (!confirm('¿Estás seguro de que deseas desvincular tu cuenta de Telegram? Podrás volver a vincularla más tarde.')) {
        return
    }
    
    const success = await unlinkTelegram()
    if (success) {
        notifySuccess('Éxito', 'Telegram desvinculado exitosamente')
    } else if (error.value) {
        toast.add({ title: 'Error', description: error.value, color: 'red' })
    }
}
</script>
