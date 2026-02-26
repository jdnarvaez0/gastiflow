<template>
  <div class="min-h-screen bg-landing-bg text-white overflow-x-hidden">
    <!-- Simple Header for Landing -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-landing-bg/80 backdrop-blur-md border-b border-gray-800">
      <div class="max-w-7xl mx-auto px-6 lg:px-24 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="flex items-center gap-2">
          <i class="fas fa-wallet text-xl text-primary"></i>
          <span class="text-lg font-bold text-primary">Gastiflow</span>
        </NuxtLink>
        
        <div class="flex items-center gap-4">
          <a 
            :href="dashboardUrl + '/login'" 
            class="text-gray-400 hover:text-white transition-colors"
          >
            Iniciar sesión
          </a>
          <a 
            :href="dashboardUrl + '/register'"
            class="px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark transition-colors"
          >
            Registrarse
          </a>
        </div>
      </div>
    </header>
    
    <!-- Main Content -->
    <main class="pt-20">
      <slot />
    </main>
    
    <!-- Simple Footer -->
    <footer class="bg-black/40 border-t border-gray-800 py-12 px-6 lg:px-24">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <i class="fas fa-wallet text-primary"></i>
          <span class="font-semibold">Gastiflow</span>
        </div>
        <p class="text-gray-500 text-sm">© 2025 Gastiflow. Todos los derechos reservados.</p>
        <div class="flex items-center gap-4">
          <a href="#" class="text-gray-400 hover:text-white transition-colors">
            <i class="fab fa-github text-xl"></i>
          </a>
          <a href="#" class="text-gray-400 hover:text-white transition-colors">
            <i class="fab fa-twitter text-xl"></i>
          </a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Landing layout - no auth required
// URL del dashboard (en producción cambiar al dominio real)
const dashboardUrl = 'http://localhost:3000'
</script>

<style>
/* Landing theme colors */
.bg-landing-bg {
  background-color: #0f0f1a;
}
.bg-landing-card {
  background-color: #1f1f35;
}
.text-primary {
  color: #4f46e5;
}
.bg-primary {
  background-color: #4f46e5;
}
.hover\:bg-primary-dark:hover {
  background-color: #4338ca;
}
.text-accent {
  color: #9333ea;
}
.bg-accent {
  background-color: #9333ea;
}
.from-accent {
  --tw-gradient-from: #9333ea;
  --tw-gradient-to: rgb(147 51 234 / 0);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}
.to-accent-light {
  --tw-gradient-to: #a855f7;
}
.text-success {
  color: #4CE1B6;
}
</style>
