<template>
    <div class="settings-container">
        <div class="settings-header">
            <h1><i class="fas fa-cog"></i> Configuración</h1>
            <p>Gestiona tu cuenta y API Key de Gemini</p>
        </div>
        
        <div class="settings-grid">
            <!-- Profile & Photo Card -->
            <div class="settings-card profile-card">
                <h2><i class="fas fa-user"></i> Perfil</h2>
                
                <!-- Avatar Section -->
                <div class="avatar-section">
                    <UserAvatar 
                        :image-url="user?.profile_picture_url" 
                        :name="user?.full_name || user?.username"
                        :username="user?.username"
                        size="xl"
                    />
                    <div class="avatar-actions">
                        <label class="btn-secondary upload-btn">
                            <i class="fas fa-camera"></i>
                            {{ user?.profile_picture_url ? 'Cambiar foto' : 'Subir foto' }}
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
                            class="btn-danger-outline"
                            :disabled="isUploadingPhoto"
                        >
                            <i class="fas fa-trash"></i>
                            Eliminar
                        </button>
                    </div>
                    <p class="hint avatar-hint">
                        <i class="fas fa-info-circle"></i>
                        JPG, PNG, GIF o WebP. Máximo 5MB.
                    </p>
                </div>
                
                <!-- Profile Info -->
                <div class="profile-info">
                    <div class="info-row">
                        <span class="label">Usuario:</span>
                        <span class="value">{{ user?.username }}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Interacciones usadas:</span>
                        <span class="value">{{ user?.interaction_count || 0 }}</span>
                    </div>
                </div>
                
                <!-- Full Name Form -->
                <form @submit.prevent="handleSaveFullName" class="name-form">
                    <div class="form-group">
                        <label for="full_name">Nombre completo</label>
                        <input 
                            type="text" 
                            id="full_name" 
                            v-model="fullName" 
                            placeholder="Ej: Juan Narvaez"
                            :disabled="isLoading"
                        />
                        <p class="hint">
                            <i class="fas fa-info-circle"></i>
                            Este nombre se usará para generar tus iniciales en el avatar
                        </p>
                    </div>
                    <button type="submit" class="btn-primary" :disabled="isLoading || !hasFullNameChanged">
                        <i class="fas fa-save"></i>
                        {{ isLoading ? 'Guardando...' : 'Guardar Nombre' }}
                    </button>
                </form>
            </div>
            
            <!-- Email Card -->
            <div class="settings-card">
                <h2><i class="fas fa-envelope"></i> Email</h2>
                <div class="email-info">
                    <div class="info-row">
                        <span class="label">Email actual:</span>
                        <span class="value">
                            {{ user?.email || 'No configurado' }}
                            <span v-if="user?.email" class="verification-badge" :class="{ 'verified': user?.email_verified }">
                                <i :class="user?.email_verified ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
                                {{ user?.email_verified ? 'Verificado' : 'No verificado' }}
                            </span>
                        </span>
                    </div>
                </div>
                
                <!-- Resend Verification Button -->
                <div v-if="user?.email && !user?.email_verified" class="resend-section">
                    <button @click="handleResendVerification" class="btn-secondary" :disabled="isResending">
                        <i class="fas fa-paper-plane"></i>
                        {{ isResending ? 'Reenviando...' : 'Reenviar email de verificación' }}
                    </button>
                </div>
                
                <!-- Change Email Form -->
                <form @submit.prevent="handleChangeEmail" class="email-form">
                    <div class="form-group">
                        <label for="new_email">
                            {{ user?.email ? 'Cambiar email' : 'Agregar email' }}
                        </label>
                        <input 
                            type="email" 
                            id="new_email" 
                            v-model="newEmail" 
                            :placeholder="user?.email || 'tu@email.com'"
                            :disabled="isLoading"
                        />
                        <p class="hint">
                            <i class="fas fa-info-circle"></i>
                            {{ user?.email ? 'Recibirás un email de verificación en la nueva dirección' : 'Recibirás un email de verificación' }}
                        </p>
                    </div>
                    
                    <button type="submit" class="btn-primary" :disabled="isLoading || !newEmail || newEmail === user?.email">
                        <i class="fas fa-save"></i>
                        {{ isLoading ? 'Guardando...' : (user?.email ? 'Cambiar Email' : 'Agregar Email') }}
                    </button>
                </form>
            </div>
            
            <!-- API Key Card -->
            <div class="settings-card">
                <h2><i class="fas fa-key"></i> API Key de Gemini</h2>
                <div class="api-status" :class="{ 'has-key': user?.has_gemini_key }">
                    <i :class="user?.has_gemini_key ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
                    {{ user?.has_gemini_key ? 'API Key configurada' : 'Sin API Key' }}
                </div>
                
                <form @submit.prevent="saveApiKey" class="api-form">
                    <div class="form-group">
                        <label for="gemini_key">
                            Nueva API Key
                        </label>
                        <input 
                            type="password" 
                            id="gemini_key" 
                            v-model="geminiApiKey" 
                            placeholder="AIza..."
                            :disabled="isLoading"
                        />
                        <p class="hint">
                            <i class="fas fa-info-circle"></i>
                            Obtén tu API Key gratis en 
                            <a href="https://aistudio.google.com/app/apikey" target="_blank">
                                Google AI Studio
                            </a>
                        </p>
                    </div>
                    
                    <button type="submit" class="btn-primary" :disabled="isLoading || !geminiApiKey">
                        <i class="fas fa-save"></i>
                        {{ isLoading ? 'Guardando...' : 'Guardar API Key' }}
                    </button>
                </form>
            </div>
            
            <!-- Telegram Card -->
            <div class="settings-card">
                <h2><i class="fab fa-telegram"></i> Telegram</h2>
                <div class="telegram-info">
                    <div class="info-row">
                        <span class="label">Estado:</span>
                        <span class="value" :class="{ 'linked': user?.telegram_id }">
                            {{ user?.telegram_id ? '✅ Vinculado' : '⚠️ No vinculado' }}
                        </span>
                    </div>
                    <div v-if="user?.telegram_id" class="info-row">
                        <span class="label">Telegram ID:</span>
                        <span class="value">{{ user.telegram_id }}</span>
                    </div>
                </div>
                
                <!-- Link Code Generation -->
                <div v-if="!user?.telegram_id" class="telegram-link-section">
                    <button 
                        @click="handleGenerateLinkCode" 
                        class="btn-primary" 
                        :disabled="isLoading || showLinkCode"
                    >
                        <i class="fas fa-qrcode"></i>
                        {{ isLoading ? 'Generando...' : 'Generar Código de Vinculación' }}
                    </button>
                    
                    <!-- Link Code Display -->
                    <div v-if="showLinkCode" class="link-code-display">
                        <div class="code-box">
                            <div class="code-label">Tu código de vinculación:</div>
                            <div class="code-value">{{ linkCode }}</div>
                            <div class="code-timer">
                                <i class="fas fa-clock"></i>
                                Expira en {{ formatTimeRemaining(linkCodeExpiry) }}
                            </div>
                        </div>
                        
                        <div class="instructions">
                            <h4><i class="fas fa-info-circle"></i> Instrucciones:</h4>
                            <ol>
                                <li>Abre Telegram y busca el bot de Gastiflow</li>
                                <li>Envía el comando: <code>/link {{ linkCode }}</code></li>
                                <li>Espera la confirmación del bot</li>
                            </ol>
                            <div class="bot-link">
                                <a :href="telegramBotUrl" target="_blank" class="btn-secondary">
                                    <i class="fab fa-telegram"></i>
                                    Abrir Bot en Telegram
                                </a>
                            </div>
                        </div>
                        
                        <div v-if="isPolling" class="polling-status">
                            <i class="fas fa-spinner fa-spin"></i>
                            Esperando vinculación...
                        </div>
                    </div>
                </div>
                
                <!-- Already Linked Message -->
                <div v-else class="linked-message">
                    <i class="fas fa-check-circle"></i>
                    Tu cuenta de Telegram está vinculada correctamente. Ahora puedes usar el bot sin límites.
                </div>
            </div>
        </div>
        
        <!-- Success/Error Messages -->
        <div v-if="successMessage" class="success-message">
            <i class="fas fa-check-circle"></i> {{ successMessage }}
        </div>
        <div v-if="error" class="error-message">
            <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>
        
        <!-- Back Button -->
        <div class="actions">
            <NuxtLink to="/" class="btn-back">
                <i class="fas fa-arrow-left"></i> Volver al Dashboard
            </NuxtLink>
            
            <button @click="handleLogout" class="btn-logout">
                <i class="fas fa-sign-out-alt"></i> Cerrar Sesión
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
const router = useRouter()
const { user, isLoading, error, updateSettings, logout, isAuthenticated, init, changeEmail, resendVerification, uploadProfilePicture, deleteProfilePicture, generateLinkCode, checkLinkStatus } = useAuth()

const geminiApiKey = ref('')
const newEmail = ref('')
const successMessage = ref<string | null>(null)
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

// Telegram bot URL (you should configure this in your .env)
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
    // Pre-fill full name if exists
    if (user.value?.full_name) {
        fullName.value = user.value.full_name
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

const saveApiKey = async () => {
    successMessage.value = null
    const success = await updateSettings({ gemini_api_key: geminiApiKey.value })
    if (success) {
        successMessage.value = 'API Key guardada correctamente'
        geminiApiKey.value = ''
    }
}

// Telegram Link Code Functions
const handleGenerateLinkCode = async () => {
    successMessage.value = null
    const response = await generateLinkCode()
    
    if (response) {
        linkCode.value = response.code
        linkCodeExpiry.value = new Date(response.expires_at)
        showLinkCode.value = true
        
        // Start polling for link status
        startPolling()
        
        // Start timer countdown
        startTimer()
    }
}

const startPolling = () => {
    isPolling.value = true
    
    // Poll every 3 seconds
    pollingInterval.value = setInterval(async () => {
        const status = await checkLinkStatus()
        
        if (status?.linked) {
            // Link successful!
            successMessage.value = '✅ ¡Telegram vinculado exitosamente!'
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
    // Update timer every second
    timerInterval.value = setInterval(() => {
        if (linkCodeExpiry.value && new Date() >= linkCodeExpiry.value) {
            // Code expired
            stopTimer()
            stopPolling()
            showLinkCode.value = false
            error.value = 'El código ha expirado. Genera uno nuevo.'
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
    successMessage.value = null
    const success = await changeEmail(newEmail.value)
    if (success) {
        successMessage.value = 'Email actualizado. Revisa tu bandeja de entrada para verificarlo.'
        newEmail.value = ''
    }
}

const handleResendVerification = async () => {
    successMessage.value = null
    isResending.value = true
    const success = await resendVerification()
    isResending.value = false
    if (success) {
        successMessage.value = 'Email de verificación reenviado exitosamente'
    }
}

const handleLogout = () => {
    logout()
    router.push('/login')
}

const handleSaveFullName = async () => {
    successMessage.value = null
    const success = await updateSettings({ full_name: fullName.value || null })
    if (success) {
        successMessage.value = 'Nombre guardado correctamente'
    }
}

const handleFileUpload = async (event: Event) => {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0]
    if (!file) return
    
    successMessage.value = null
    isUploadingPhoto.value = true
    
    const success = await uploadProfilePicture(file)
    
    isUploadingPhoto.value = false
    if (success) {
        successMessage.value = 'Foto de perfil actualizada'
    }
    
    // Reset input
    target.value = ''
}

const handleDeletePhoto = async () => {
    successMessage.value = null
    isUploadingPhoto.value = true
    
    const success = await deleteProfilePicture()
    
    isUploadingPhoto.value = false
    if (success) {
        successMessage.value = 'Foto de perfil eliminada'
    }
}

</script>

<style scoped>
.settings-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

.settings-header {
    margin-bottom: 2rem;
}

.settings-header h1 {
    font-size: 1.75rem;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.settings-header p {
    color: var(--text-secondary);
}

.settings-grid {
    display: grid;
    gap: 1.5rem;
}

.settings-card {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid var(--border-color);
}

.settings-card h2 {
    font-size: 1.125rem;
    color: var(--text-primary);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.profile-info, .telegram-info {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.email-info {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.verification-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-left: 0.5rem;
    background: rgba(239, 68, 68, 0.1);
    color: #f87171;
}

.verification-badge.verified {
    background: rgba(34, 197, 94, 0.1);
    color: #4ade80;
}

.resend-section {
    margin: 1rem 0;
}

.email-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
}


.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.info-row .label {
    color: var(--text-secondary);
}

.info-row .value {
    color: var(--text-primary);
    font-weight: 500;
}

.api-status {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    background: rgba(239, 68, 68, 0.1);
    color: #f87171;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.api-status.has-key {
    background: rgba(34, 197, 94, 0.1);
    color: #4ade80;
}

.api-form, .telegram-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-group label {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.form-group input {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 1rem;
}

.form-group input:focus {
    outline: none;
    border-color: var(--accent-primary);
}

.hint {
    font-size: 0.75rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 0.375rem;
}

.hint a {
    color: var(--accent-primary);
    text-decoration: none;
}

.hint a:hover {
    text-decoration: underline;
}

.btn-primary, .btn-secondary {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: none;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    transition: all 0.2s;
}

.btn-primary {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    color: white;
}

.btn-secondary {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}

.btn-primary:hover:not(:disabled), .btn-secondary:hover:not(:disabled) {
    transform: translateY(-1px);
}

.btn-primary:disabled, .btn-secondary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.success-message, .error-message {
    margin-top: 1.5rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.success-message {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #4ade80;
}

.error-message {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #f87171;
}

.actions {
    margin-top: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.btn-back {
    color: var(--text-secondary);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: color 0.2s;
}

.btn-back:hover {
    color: var(--text-primary);
}

.btn-logout {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid rgba(239, 68, 68, 0.3);
    background: rgba(239, 68, 68, 0.1);
    color: #f87171;
    font-size: 0.875rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s;
}

.btn-logout:hover {
    background: rgba(239, 68, 68, 0.2);
}

/* Avatar Section Styles */
.profile-card {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--bg-secondary);
    border-radius: 12px;
}

.avatar-actions {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    justify-content: center;
}

.upload-btn {
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.upload-btn:hover {
    transform: translateY(-1px);
}

.btn-danger-outline {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid rgba(239, 68, 68, 0.3);
    background: transparent;
    color: #f87171;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s;
}

.btn-danger-outline:hover:not(:disabled) {
    background: rgba(239, 68, 68, 0.1);
}

.btn-danger-outline:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.avatar-hint {
    text-align: center;
}

.name-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
}

/* Telegram Link Code Styles */
.telegram-link-section {
    margin-top: 1rem;
}

.link-code-display {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.code-box {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
    border: 2px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
}

.code-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
}

.code-value {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: 0.5rem;
    color: var(--accent-primary);
    font-family: 'Courier New', monospace;
    margin-bottom: 0.75rem;
}

.code-timer {
    font-size: 0.875rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.instructions {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 1.5rem;
}

.instructions h4 {
    font-size: 1rem;
    color: var(--text-primary);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.instructions ol {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
}

.instructions li {
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
}

.instructions code {
    background: rgba(99, 102, 241, 0.1);
    color: var(--accent-primary);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-weight: 600;
}

.bot-link {
    margin-top: 1rem;
}

.polling-status {
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
    padding: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    color: #60a5fa;
    font-weight: 500;
}

.polling-status i {
    font-size: 1.25rem;
}

.linked-message {
    margin-top: 1rem;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 8px;
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #4ade80;
}

.linked-message i {
    font-size: 1.5rem;
}

.value.linked {
    color: #4ade80;
    font-weight: 600;
}
</style>
