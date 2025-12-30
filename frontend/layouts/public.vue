<template>
    <div class="public-layout">
        <!-- Simple header for public pages -->
        <header class="public-header">
            <NuxtLink to="/" class="logo">
                <i class="fas fa-wallet"></i>
                <span>Gastiflow</span>
            </NuxtLink>
            <nav class="public-nav">
                <NuxtLink to="/login" class="nav-link">Iniciar Sesión</NuxtLink>
                <NuxtLink to="/register" class="nav-link btn-register">Registrarse</NuxtLink>
            </nav>
        </header>

        <!-- Main content -->
        <main class="public-main">
            <slot />
        </main>

        <!-- Footer -->
        <footer class="public-footer">
            <p>&copy; 2025 Gastiflow. Gestiona tus finanzas de forma inteligente.</p>
        </footer>
    </div>
</template>

<script setup lang="ts">
const { isAuthenticated } = useAuth()

// If user is already authenticated and on landing, optionally redirect to dashboard
// This is commented out to allow authenticated users to view landing
// onMounted(() => {
//     if (isAuthenticated.value) {
//         navigateTo('/')
//     }
// })
</script>

<style scoped>
.public-layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

.public-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 2rem;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    background: rgba(17, 17, 27, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent-primary);
    text-decoration: none;
    transition: transform 0.2s ease;
}

.logo:hover {
    transform: scale(1.02);
}

.logo i {
    font-size: 1.75rem;
}

.public-nav {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.nav-link {
    padding: 0.625rem 1.25rem;
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.nav-link:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
}

.btn-register {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    color: white !important;
}

.btn-register:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(147, 51, 234, 0.4);
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
}

.public-main {
    flex: 1;
    margin-top: 80px;
}

.public-footer {
    text-align: center;
    padding: 2rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
    border-top: 1px solid var(--border-color);
}

@media (max-width: 768px) {
    .public-header {
        padding: 1rem;
    }
    
    .logo span {
        display: none;
    }
    
    .nav-link {
        padding: 0.5rem 0.75rem;
        font-size: 0.875rem;
    }
}
</style>
