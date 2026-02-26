<template>
  <UCard :ui="{ body: { padding: 'p-6' }, ring: '', shadow: 'shadow-sm' }" class="w-full h-full border border-gray-100 dark:border-gray-800 transition-all hover:scale-[1.02] hover:shadow-md cursor-default">
    <div class="flex justify-between items-start">
      <div>
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ title }}</p>
        <h3 class="text-2xl font-bold text-gray-900 dark:text-white mt-2">{{ amount }}</h3>
        <p v-if="subtext" class="text-xs mt-2 font-medium" :class="subtextClass">
          {{ subtext }}
        </p>
      </div>
      <div class="p-2.5 rounded-xl bg-gray-50 dark:bg-gray-800">
        <UIcon :name="icon" class="w-5 h-5 text-gray-400 dark:text-gray-500" />
      </div>
    </div>
  </UCard>
</template>

<script setup>
defineProps({
  title: String,
  amount: String,
  subtext: String,
  subtextClass: String,
  icon: String
})
</script>
