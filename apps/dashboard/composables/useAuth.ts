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
    preferred_currency: string
    timezone: string
    language: string
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
    full_name?: string
}

export interface UserSettings {
    email?: string | null
    gemini_api_key?: string | null
    telegram_id?: string | null
    full_name?: string | null
    preferred_currency?: string | null
    timezone?: string | null
    language?: string | null
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
    const isLoggingOut = useState<boolean>('auth_logging_out', () => false)
    const error = useState<string | null>('auth_error', () => null)

    // Initialize - check if we have a token and fetch user
    const init = async () => {
        if (process.client && token.value) {
            await fetchUser()
        }
    }

    // Helper to format error messages
    const formatError = (err: any): string => {
        // Si no hay error
        if (!err) return 'Ha ocurrido un error inesperado'

        // Si es un string, devolverlo directamente
        if (typeof err === 'string') return err

        // Manejar errores de $fetch de Nuxt
        if (err.data) {
            const detail = err.data.detail || err.data.message || err.data.error

            // Si el detalle es un string
            if (typeof detail === 'string') return detail

            // Si el detalle es un array (errores de validación Pydantic)
            if (Array.isArray(detail)) {
                return detail.map((item: any) => {
                    if (item.msg) {
                        let message = item.msg
                        // Limpiar prefijo "Value error, " si existe
                        if (message.startsWith('Value error, ')) {
                            message = message.replace('Value error, ', '')
                        }

                        // Agregar contexto del campo si está disponible
                        if (item.loc && Array.isArray(item.loc)) {
                            const field = item.loc[item.loc.length - 1]
                            if (field && field !== 'body') {
                                const fieldTranslations: Record<string, string> = {
                                    'username': 'Usuario',
                                    'password': 'Contraseña',
                                    'email': 'Email',
                                    'full_name': 'Nombre completo',
                                    'telegram_id': 'ID de Telegram'
                                }
                                const fieldName = fieldTranslations[String(field)] || String(field).charAt(0).toUpperCase() + String(field).slice(1)
                                return `${fieldName}: ${message}`
                            }
                        }
                        return message
                    }
                    return JSON.stringify(item)
                }).join('. ')
            }

            // Si hay un hint en la respuesta, usarlo
            if (err.data.hint) {
                return err.data.hint
            }

            // Si hay error_id, mostrarlo para debugging
            if (err.data.error_id) {
                console.error(`Error ID: ${err.data.error_id}`)
            }
        }

        // Errores de red
        if (err.name === 'TypeError' || err.message?.includes('fetch') || err.message?.includes('network')) {
            return 'Error de conexión: No se pudo conectar con el servidor. Verifica tu conexión a internet.'
        }

        // Errores de CORS
        if (err.statusCode === 0 || err.status === 0) {
            return 'Error de conexión: Problema con CORS o el servidor no responde. Verifica la configuración.'
        }

        // Timeout
        if (err.name === 'AbortError' || err.message?.includes('timeout')) {
            return 'La operación tomó demasiado tiempo. Por favor intenta nuevamente.'
        }

        // Errores HTTP específicos
        if (err.statusCode === 429) {
            return 'Demasiadas solicitudes. Por favor espera un momento antes de intentar nuevamente.'
        }

        if (err.statusCode === 401) {
            return 'Usuario o contraseña incorrectos'
        }

        if (err.statusCode === 403) {
            return 'No tienes permiso para realizar esta acción'
        }

        if (err.statusCode === 404) {
            return 'El recurso solicitado no fue encontrado'
        }

        if (err.statusCode === 422) {
            return 'Los datos proporcionados no son válidos. Por favor verifica la información.'
        }

        if (err.statusCode >= 500) {
            return 'Error del servidor. Por favor intenta más tarde o contacta soporte.'
        }

        // Intentar obtener mensaje del error
        if (err.message && typeof err.message === 'string') {
            return err.message
        }

        // Fallback: convertir a string
        return 'Ha ocurrido un error inesperado. Por favor intenta nuevamente.'
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
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'ngrok-skip-browser-warning': 'true'
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
            error.value = formatError(e) || 'Error al iniciar sesión'
            console.error('Login error:', e)
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
                headers: {
                    'ngrok-skip-browser-warning': 'true'
                },
                body: data
            })

            // Auto-login after registration
            return await login({ username: data.username, password: data.password })
        } catch (e: any) {
            error.value = formatError(e) || 'Error al registrarse'
            console.error('Register error:', e)
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
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
                }
            })
            user.value = userData
        } catch (e: any) {
            // Solo hacer logout si el token es inválido (401), no por errores de red
            if (e.statusCode === 401 || e.status === 401) {
                console.log('Token inválido o expirado, cerrando sesión')
                logout()
            } else {
                // Para otros errores, solo loguear pero mantener la sesión
                console.error('Error fetching user:', e)
            }
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
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
                },
                body: settings
            })
            user.value = updatedUser
            return true
        } catch (e: any) {
            error.value = formatError(e) || 'Error al actualizar configuración'
            return false
        } finally {
            isLoading.value = false
        }
    }

    // Logout
    const logout = async () => {
        isLoggingOut.value = true

        // Small delay to show the loading state
        await new Promise(resolve => setTimeout(resolve, 300))

        token.value = null
        user.value = null
        if (process.client) {
            localStorage.removeItem('gastiflow_token')
            // Redirect to landing page after logout
            const landingUrl = config.public.landingUrl || 'http://localhost:3001'
            window.location.href = landingUrl as string
        }
    }

    // Get auth headers for API calls
    const getAuthHeaders = () => {
        const headers: Record<string, string> = {
            'ngrok-skip-browser-warning': 'true'
        }
        if (token.value) {
            headers['Authorization'] = `Bearer ${token.value}`
        }
        return headers
    }

    // Verify email with token
    const verifyEmail = async (verificationToken: string) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await $fetch<{ message: string; already_verified: boolean }>('/api/verify-email', {
                baseURL: apiUrl,
                headers: {
                    'ngrok-skip-browser-warning': 'true'
                },
                params: { token: verificationToken }
            })

            // Refresh user data if logged in
            if (token.value) {
                await fetchUser()
            }

            return { success: true, alreadyVerified: response.already_verified }
        } catch (e: any) {
            error.value = formatError(e) || 'Error al verificar el email'
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
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
                }
            })
            return true
        } catch (e: any) {
            error.value = formatError(e) || 'Error al reenviar email de verificación'
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
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
                },
                body: { email: newEmail }
            })
            user.value = updatedUser
            return true
        } catch (e: any) {
            error.value = formatError(e) || 'Error al cambiar email'
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
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
                },
                body: formData
            })
            user.value = updatedUser
            return true
        } catch (e: any) {
            error.value = formatError(e) || 'Error al subir la foto de perfil'
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
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
                }
            })
            user.value = updatedUser
            return true
        } catch (e: any) {
            error.value = formatError(e) || 'Error al eliminar la foto de perfil'
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
            const response = await $fetch<{ code: string; expires_at: string }>('/api/telegram/link-code', {
                baseURL: apiUrl,
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
                }
            })
            return response
        } catch (e: any) {
            error.value = formatError(e) || 'Error al generar código de vinculación'
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
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
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

    // Unlink Telegram account
    const unlinkTelegram = async () => {
        if (!token.value) return false

        isLoading.value = true
        error.value = null

        try {
            await $fetch('/api/telegram/unlink', {
                baseURL: apiUrl,
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token.value}`,
                    'ngrok-skip-browser-warning': 'true'
                }
            })

            // Update local user state
            if (user.value) {
                user.value.telegram_id = null
            }

            return true
        } catch (e: any) {
            error.value = formatError(e) || 'Error al desvincular Telegram'
            return false
        } finally {
            isLoading.value = false
        }
    }

    return {
        user,
        token,
        isAuthenticated,
        isLoading,
        isLoggingOut,
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
        checkLinkStatus,
        unlinkTelegram
    }
}
