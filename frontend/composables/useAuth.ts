/**
 * Authentication composable for managing user auth state
 */

export interface User {
    id: number
    username: string
    email: string | null
    telegram_id: string | null
    has_gemini_key: boolean
    interaction_count: number
    is_active: boolean
    email_verified: boolean
    full_name: string | null
    profile_picture_url: string | null
}

export interface LoginCredentials {
    username: string
    password: string
}

export interface RegisterData {
    username: string
    password: string
    email?: string
    telegram_id?: string
}

export interface UserSettings {
    email?: string | null
    gemini_api_key?: string | null
    telegram_id?: string | null
    full_name?: string | null
}

export const useAuth = () => {
    const config = useRuntimeConfig()
    const apiUrl = config.public.apiUrl

    // State
    const user = useState<User | null>('auth_user', () => null)
    const token = useState<string | null>('auth_token', () => {
        if (process.client) {
            return localStorage.getItem('gastiflow_token')
        }
        return null
    })
    const isAuthenticated = computed(() => !!token.value && !!user.value)
    const isLoading = useState<boolean>('auth_loading', () => false)
    const error = useState<string | null>('auth_error', () => null)

    // Initialize - check if we have a token and fetch user
    const init = async () => {
        if (process.client && token.value) {
            await fetchUser()
        }
    }

    // Helper to format error messages
    const formatError = (detail: any): string => {
        if (!detail) return 'Ha ocurrido un error inesperado'

        // If it's already a string, return it
        if (typeof detail === 'string') return detail

        // If it's an array (typically Pydantic validation errors)
        if (Array.isArray(detail)) {
            return detail.map(err => {
                if (err.msg) {
                    // Start with the message
                    let message = err.msg

                    // Add location context if available and relevant (not for "body")
                    if (err.loc && Array.isArray(err.loc)) {
                        const field = err.loc[err.loc.length - 1]
                        if (field && field !== 'body') {
                            // Translate common field names if possible, or just capitalize
                            const fieldName = String(field).charAt(0).toUpperCase() + String(field).slice(1)
                            return `${fieldName}: ${message}`
                        }
                    }
                    return message
                }
                return JSON.stringify(err)
            }).join('. ')
        }

        // Fallback for objects
        return JSON.stringify(detail)
    }

    // Login
    const login = async (credentials: LoginCredentials) => {
        isLoading.value = true
        error.value = null

        try {
            const formData = new URLSearchParams()
            formData.append('username', credentials.username)
            formData.append('password', credentials.password)

            const response = await $fetch<{ access_token: string; token_type: string }>('/api/login', {
                baseURL: apiUrl,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData.toString()
            })

            token.value = response.access_token
            if (process.client) {
                localStorage.setItem('gastiflow_token', response.access_token)
            }

            await fetchUser()
            return true
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al iniciar sesión'
            return false
        } finally {
            isLoading.value = false
        }
    }

    // Register
    const register = async (data: RegisterData) => {
        isLoading.value = true
        error.value = null

        try {
            await $fetch<User>('/api/register', {
                baseURL: apiUrl,
                method: 'POST',
                body: data
            })

            // Auto-login after registration
            return await login({ username: data.username, password: data.password })
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al registrarse'
            return false
        } finally {
            isLoading.value = false
        }
    }

    // Fetch current user
    const fetchUser = async () => {
        if (!token.value) return

        try {
            const userData = await $fetch<User>('/api/me', {
                baseURL: apiUrl,
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            })
            user.value = userData
        } catch (e) {
            // Token invalid - logout
            logout()
        }
    }

    // Update settings
    const updateSettings = async (settings: UserSettings) => {
        if (!token.value) return false

        isLoading.value = true
        error.value = null

        try {
            const updatedUser = await $fetch<User>('/api/settings', {
                baseURL: apiUrl,
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token.value}`
                },
                body: settings
            })
            user.value = updatedUser
            return true
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al actualizar configuración'
            return false
        } finally {
            isLoading.value = false
        }
    }

    // Logout
    const logout = () => {
        token.value = null
        user.value = null
        if (process.client) {
            localStorage.removeItem('gastiflow_token')
        }
    }

    // Get auth headers for API calls
    const getAuthHeaders = () => {
        if (!token.value) return {}
        return {
            'Authorization': `Bearer ${token.value}`
        }
    }

    // Verify email with token
    const verifyEmail = async (verificationToken: string) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await $fetch<{ message: string; already_verified: boolean }>('/api/verify-email', {
                baseURL: apiUrl,
                params: { token: verificationToken }
            })

            // Refresh user data if logged in
            if (token.value) {
                await fetchUser()
            }

            return { success: true, alreadyVerified: response.already_verified }
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al verificar el email'
            return { success: false, alreadyVerified: false }
        } finally {
            isLoading.value = false
        }
    }


    // Resend verification email
    const resendVerification = async () => {
        if (!token.value) return false

        isLoading.value = true
        error.value = null

        try {
            await $fetch('/api/resend-verification', {
                baseURL: apiUrl,
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            })
            return true
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al reenviar email de verificación'
            return false
        } finally {
            isLoading.value = false
        }
    }

    // Change email (will require re-verification)
    const changeEmail = async (newEmail: string) => {
        if (!token.value) return false

        isLoading.value = true
        error.value = null

        try {
            const updatedUser = await $fetch<User>('/api/settings', {
                baseURL: apiUrl,
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token.value}`
                },
                body: { email: newEmail }
            })
            user.value = updatedUser
            return true
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al cambiar email'
            return false
        } finally {
            isLoading.value = false
        }
    }

    // Upload profile picture
    const uploadProfilePicture = async (file: File) => {
        if (!token.value) return false

        isLoading.value = true
        error.value = null

        try {
            const formData = new FormData()
            formData.append('file', file)

            const updatedUser = await $fetch<User>('/api/profile-picture', {
                baseURL: apiUrl,
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token.value}`
                },
                body: formData
            })
            user.value = updatedUser
            return true
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al subir la foto de perfil'
            return false
        } finally {
            isLoading.value = false
        }
    }

    // Delete profile picture
    const deleteProfilePicture = async () => {
        if (!token.value) return false

        isLoading.value = true
        error.value = null

        try {
            const updatedUser = await $fetch<User>('/api/profile-picture', {
                baseURL: apiUrl,
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            })
            user.value = updatedUser
            return true
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al eliminar la foto de perfil'
            return false
        } finally {
            isLoading.value = false
        }
    }

    // Generate Telegram link code
    const generateLinkCode = async () => {
        if (!token.value) return null

        isLoading.value = true
        error.value = null

        try {
            const response = await $fetch<{ code: string; expires_at: string }>('/api/telegram/generate-link-code', {
                baseURL: apiUrl,
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            })
            return response
        } catch (e: any) {
            error.value = formatError(e?.data?.detail) || 'Error al generar código de vinculación'
            return null
        } finally {
            isLoading.value = false
        }
    }

    // Check Telegram link status
    const checkLinkStatus = async () => {
        if (!token.value) return null

        try {
            const response = await $fetch<{ linked: boolean; telegram_id: string | null }>('/api/telegram/link-status', {
                baseURL: apiUrl,
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            })

            // Update user if linked
            if (response.linked && user.value) {
                user.value.telegram_id = response.telegram_id
            }

            return response
        } catch (e: any) {
            return null
        }
    }

    return {
        user,
        token,
        isAuthenticated,
        isLoading,
        error,
        init,
        login,
        register,
        logout,
        fetchUser,
        updateSettings,
        getAuthHeaders,
        verifyEmail,
        resendVerification,
        changeEmail,
        uploadProfilePicture,
        deleteProfilePicture,
        generateLinkCode,
        checkLinkStatus
    }
}
