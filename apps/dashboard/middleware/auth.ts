/**
 * Authentication middleware for Nuxt
 * Protects routes that require authentication
 */

export default defineNuxtRouteMiddleware((to, from) => {
    // Public routes that don't require authentication
    const publicRoutes = ['/', '/login', '/register', '/verify-email']

    // Check if the route is public (exact match for '/', startsWith for others)
    const isPublic = publicRoutes.some(route => {
        if (route === '/') {
            return to.path === '/'
        }
        return to.path.startsWith(route)
    })

    if (isPublic) {
        return
    }

    // Only run on client side
    if (process.client) {
        const token = localStorage.getItem('gastiflow_token')

        // If no token and trying to access protected route, redirect to landing
        if (!token) {
            return navigateTo('http://localhost:3001', { external: true })
        }
    }
})
