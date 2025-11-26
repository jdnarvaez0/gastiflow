<template>
  <UCard :ui="{ body: { padding: 'p-0' }, ring: '', shadow: 'shadow-sm' }" class="w-full border border-gray-100 dark:border-gray-800 overflow-hidden">
    <template #header>
      <div class="flex justify-between items-center px-6 py-4 border-b border-gray-100 dark:border-gray-800">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white">Movimientos Recientes</h3>
        <UButton variant="link" color="primary" class="text-sm font-medium hover:text-primary-600 p-0">Ver Todos</UButton>
      </div>
    </template>
    
    <UTable :rows="processedTransactions" :columns="columns" :ui="{ td: { padding: 'px-6 py-4' }, th: { padding: 'px-6 py-3', color: 'text-gray-500 dark:text-gray-400', font: 'font-medium' } }">
      <template #icon-data="{ row }">
         <div :class="['p-2.5 rounded-xl inline-flex items-center justify-center', row.iconBg]">
            <UIcon :name="row.icon" :class="['w-5 h-5', row.iconColor]" />
         </div>
      </template>
      
      <template #description-data="{ row }">
        <div>
            <p class="font-semibold text-gray-900 dark:text-white text-sm">{{ row.description }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ row.subDescription }}</p>
        </div>
      </template>

      <template #category-data="{ row }">
        <span class="text-sm text-gray-500 dark:text-gray-400">{{ row.category }}</span>
      </template>

      <template #date-data="{ row }">
        <span class="text-sm text-gray-500 dark:text-gray-400">{{ row.date }}</span>
      </template>

      <template #amount-data="{ row }">
        <span :class="['text-sm font-bold', row.amountClass]">{{ row.amount }}</span>
      </template>
    </UTable>
  </UCard>
</template>

<script setup>
const props = defineProps({
  transactions: {
    type: Array,
    default: () => []
  }
})

const columns = [
  { key: 'icon', label: '', id: 'icon' },
  { key: 'description', label: 'Descripción', id: 'description' },
  { key: 'category', label: 'Categoría', id: 'category' },
  { key: 'date', label: 'Fecha', id: 'date' },
  { key: 'amount', label: 'Monto', id: 'amount' }
]

const getCategoryIcon = (category) => {
  const icons = {
    'Comida': 'i-heroicons-shopping-cart',
    'Transporte': 'i-heroicons-truck',
    'Vivienda': 'i-heroicons-home',
    'Ocio': 'i-heroicons-film',
    'Salud': 'i-heroicons-heart',
    'Ingresos': 'i-heroicons-briefcase',
    'Otros': 'i-heroicons-tag'
  }
  return icons[category] || 'i-heroicons-currency-dollar'
}

const processedTransactions = computed(() => {
  return props.transactions.map(t => {
    const isIncome = t.transaction_type === 'income'
    const amountFormatted = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(t.amount)
    
    return {
      id: t.id,
      icon: getCategoryIcon(t.category),
      iconBg: isIncome ? 'bg-green-100 dark:bg-green-900/20' : 'bg-red-100 dark:bg-red-900/20',
      iconColor: isIncome ? 'text-green-600' : 'text-red-600',
      description: t.description,
      subDescription: t.category,
      category: t.category,
      date: new Date(t.date).toLocaleDateString('es-CO'),
      amount: (isIncome ? '+' : '-') + amountFormatted,
      amountClass: isIncome ? 'text-green-600 font-medium' : 'text-red-600 font-medium'
    }
  })
})
</script>
