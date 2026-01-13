<template>
  <aside class="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 hidden md:flex flex-col">
    <div class="p-6">
      <div class="flex items-center gap-2">
        <i class="fas fa-wallet text-xl text-primary-600"></i>
        <span class="text-lg font-bold text-primary-600">Gastiflow</span>
      </div>
    </div>
    
    <nav class="flex-1 px-4 space-y-2">
      <NuxtLink to="/" class="flex items-center px-4 py-3 text-gray-600 dark:text-gray-400 rounded-xl transition-colors hover:bg-gray-50 dark:hover:bg-gray-800" active-class="bg-primary-50 dark:bg-primary-900/10 text-primary-600 dark:text-primary-400 font-medium">
        <UIcon name="i-heroicons-squares-2x2" class="w-5 h-5 mr-3" />
        Dashboard
      </NuxtLink>

      <NuxtLink to="/movimientos" class="flex items-center px-4 py-3 text-gray-600 dark:text-gray-400 rounded-xl transition-colors hover:bg-gray-50 dark:hover:bg-gray-800" active-class="bg-primary-50 dark:bg-primary-900/10 text-primary-600 dark:text-primary-400 font-medium">
        <UIcon name="i-heroicons-list-bullet" class="w-5 h-5 mr-3" />
        Movimientos
      </NuxtLink>

      <NuxtLink to="/reportes" class="flex items-center px-4 py-3 text-gray-600 dark:text-gray-400 rounded-xl transition-colors hover:bg-gray-50 dark:hover:bg-gray-800" active-class="bg-primary-50 dark:bg-primary-900/10 text-primary-600 dark:text-primary-400 font-medium">
        <UIcon name="i-heroicons-chart-pie" class="w-5 h-5 mr-3" />
        Reportes
      </NuxtLink>

      <NuxtLink to="/cuentas" class="flex items-center px-4 py-3 text-gray-600 dark:text-gray-400 rounded-xl transition-colors hover:bg-gray-50 dark:hover:bg-gray-800" active-class="bg-primary-50 dark:bg-primary-900/10 text-primary-600 dark:text-primary-400 font-medium">
        <UIcon name="i-heroicons-credit-card" class="w-5 h-5 mr-3" />
        Cuentas
      </NuxtLink>

      <NuxtLink to="/categorias" class="flex items-center px-4 py-3 text-gray-600 dark:text-gray-400 rounded-xl transition-colors hover:bg-gray-50 dark:hover:bg-gray-800" active-class="bg-primary-50 dark:bg-primary-900/10 text-primary-600 dark:text-primary-400 font-medium">
        <UIcon name="i-heroicons-tag" class="w-5 h-5 mr-3" />
        Categorías
      </NuxtLink>
    </nav>

    <div class="p-4 border-t border-gray-200 dark:border-gray-800 space-y-2">
      <button class="flex items-center w-full px-4 py-3 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-xl transition-colors">
        <UIcon name="i-heroicons-cog-6-tooth" class="w-5 h-5 mr-3" />
        Ajustes
      </button>
      <button class="flex items-center w-full px-4 py-3 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/10 rounded-xl transition-colors">
        <UIcon name="i-heroicons-arrow-left-on-rectangle" class="w-5 h-5 mr-3" />
        Cerrar sesión
      </button>
    </div>
  </aside>
</template>
