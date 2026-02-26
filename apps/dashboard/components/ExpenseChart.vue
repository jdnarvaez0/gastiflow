<template>
  <UCard>
    <template #header>
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Resumen de Gastos</h3>
        <div class="flex space-x-2">
           <UButton size="xs" color="gray" variant="solid">Este Mes</UButton>
           <UButton size="xs" color="gray" variant="ghost">Últimos 6 meses</UButton>
        </div>
      </div>
    </template>
    <div class="flex items-end justify-between h-64 space-x-4 mt-4">
      <div v-for="(item, index) in chartData" :key:="index" class="flex flex-col items-center flex-1 h-full justify-end group">
        <div class="w-full rounded-t-lg transition-all duration-300 hover:opacity-80 relative" 
             :class="item.color" 
             :style="{ height: item.percentage + '%' }">
             <div class="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs py-1 px-2 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                 {{ item.value }}
             </div>
        </div>
        <span class="text-xs text-gray-500 mt-2 truncate w-full text-center">{{ item.label }}</span>
      </div>
    </div>
  </UCard>
</template>

<script setup>
const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  }
})

const chartData = computed(() => {
  if (!props.categories.length) return []
  
  const total = props.categories.reduce((acc, curr) => acc + curr.amount, 0)
  const max = Math.max(...props.categories.map(c => c.amount))
  
  const colors = ['bg-red-300', 'bg-blue-300', 'bg-yellow-300', 'bg-purple-300', 'bg-green-300', 'bg-indigo-300', 'bg-pink-300', 'bg-orange-300']

  return props.categories.map((item, index) => ({
    label: item.category,
    value: new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(item.amount),
    percentage: max > 0 ? (item.amount / max) * 100 : 0,
    color: colors[index % colors.length]
  }))
})
</script>
