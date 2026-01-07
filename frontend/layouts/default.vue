<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <nav class="fixed top-0 left-0 h-screen w-56 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 px-3 py-4 flex flex-col">
        <div class="flex items-center gap-2 text-primary font-bold text-lg mb-4">
            <i class="fa-solid fa-wallet"></i> Gastiflow
        </div>
        <ul class="flex-1 space-y-1">
            <li>
                <NuxtLink to="/dashboard" active-class="!bg-primary !text-white" class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
                    <i class="fa-solid fa-chart-pie"></i> Dashboard
                </NuxtLink>
            </li>
            <li>
                <a href="#" class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
                    <i class="fa-solid fa-list"></i> Movimientos
                </a>
            </li>
            <li>
                <a href="#" class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
                    <i class="fa-solid fa-chart-line"></i> Reportes
                </a>
            </li>
            <li>
                <a href="#" class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
                    <i class="fa-solid fa-credit-card"></i> Cuentas
                </a>
            </li>
            <li>
                <a href="#" class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
                    <i class="fa-solid fa-tags"></i> Categorías
                </a>
            </li>
        </ul>
        
        <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
            <ul class="space-y-1">
                <li v-if="isAuthenticated">
                    <NuxtLink to="/settings" active-class="!bg-primary !text-white" class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
                        <i class="fa-solid fa-gear"></i> Ajustes
                    </NuxtLink>
                </li>
                <li v-if="isAuthenticated">
                    <a href="#" @click.prevent="handleLogout" class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
                        <i class="fa-solid fa-right-from-bracket"></i> Cerrar sesión
                    </a>
                </li>
                <li v-if="!isAuthenticated">
                    <NuxtLink to="/login" class="flex items-center gap-2 px-3 py-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-primary hover:text-white text-sm transition-colors">
                        <i class="fa-solid fa-sign-in-alt"></i> Iniciar sesión
                    </NuxtLink>
                </li>
            </ul>
            <div v-if="isAuthenticated && user" class="flex items-center gap-2 px-3 py-3 text-gray-500 dark:text-gray-400 text-sm border-t border-gray-200 dark:border-gray-700 mt-2">
                <i class="fa-solid fa-user-circle text-xl text-primary"></i>
                <span>{{ user.username }}</span>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="ml-56 flex-1 p-8 bg-gray-100 dark:bg-gray-900 min-h-screen">
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
