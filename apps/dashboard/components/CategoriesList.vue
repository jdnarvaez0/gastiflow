<template>
  <UCard>
    <template #header>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Categorías</h3>
    </template>
    <div class="space-y-4">
      <div v-for="(category, index) in processedCategories" :key="index" class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-2 h-2 rounded-full" :class="category.color"></div>
          <span class="text-gray-700 dark:text-gray-200">{{ category.name }}</span>
        </div>
        <span class="font-medium text-gray-900 dark:text-white">{{ category.amount }}</span>
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

const colors = ['bg-yellow-400', 'bg-blue-400', 'bg-purple-400', 'bg-red-400', 'bg-indigo-400', 'bg-green-400', 'bg-pink-400', 'bg-orange-400']

const processedCategories = computed(() => {
  return props.categories.map((cat, index) => ({
    name: cat.category,
    amount: new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(cat.amount),
    color: colors[index % colors.length]
  }))
})
</script>
