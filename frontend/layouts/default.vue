<template>
  <div>
    <!-- Sidebar -->
    <nav class="sidebar">
        <div class="logo">
            <i class="fa-solid fa-wallet"></i> Gastiflow
        </div>
        <ul class="nav-links">
            <li><NuxtLink to="/" active-class="active"><i class="fa-solid fa-chart-pie"></i> Dashboard</NuxtLink></li>
            <li><a href="#"><i class="fa-solid fa-list"></i> Movimientos</a></li>
            <li><a href="#"><i class="fa-solid fa-chart-line"></i> Reportes</a></li>
            <li><a href="#"><i class="fa-solid fa-credit-card"></i> Cuentas</a></li>
            <li><a href="#"><i class="fa-solid fa-tags"></i> Categorías</a></li>
        </ul>
        
        <div class="sidebar-footer">
            <ul class="nav-links">
                <li v-if="isAuthenticated">
                    <NuxtLink to="/settings" active-class="active">
                        <i class="fa-solid fa-gear"></i> Ajustes
                    </NuxtLink>
                </li>
                <li v-if="isAuthenticated">
                    <a href="#" @click.prevent="handleLogout">
                        <i class="fa-solid fa-right-from-bracket"></i> Cerrar sesión
                    </a>
                </li>
                <li v-if="!isAuthenticated">
                    <NuxtLink to="/login">
                        <i class="fa-solid fa-sign-in-alt"></i> Iniciar sesión
                    </NuxtLink>
                </li>
            </ul>
            <div v-if="isAuthenticated && user" class="user-info">
                <i class="fa-solid fa-user-circle"></i>
                <span>{{ user.username }}</span>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
        <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const { user, isAuthenticated, logout, init } = useAuth()

onMounted(() => {
    init()
})

const handleLogout = () => {
    logout()
    router.push('/login')
}
</script>

<style scoped>
.user-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
    border-top: 1px solid var(--border-color);
    margin-top: 0.5rem;
}

.user-info i {
    font-size: 1.25rem;
    color: var(--accent-primary);
}
</style>
