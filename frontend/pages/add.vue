<template>
  <div class="container mx-auto p-4 max-w-lg">
    <h1 class="text-3xl font-bold mb-6">Add New Expense</h1>

    <form @submit.prevent="submitExpense" class="bg-white p-6 rounded-lg shadow space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Amount</label>
        <input v-model="form.amount" type="number" step="0.01" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Description</label>
        <input v-model="form.description" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Category</label>
        <select v-model="form.category" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
          <option value="Comida">Comida</option>
          <option value="Transporte">Transporte</option>
          <option value="Servicios">Servicios</option>
          <option value="Salud">Salud</option>
          <option value="Entretenimiento">Entretenimiento</option>
          <option value="Educación">Educación</option>
          <option value="Otros">Otros</option>
          <option value="Ingreso">Ingreso</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Type</label>
        <select v-model="form.transaction_type" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Date</label>
        <input v-model="form.date" type="date" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
      </div>

      <div class="flex justify-end space-x-3 pt-4">
        <NuxtLink to="/" class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded">Cancel</NuxtLink>
        <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">Save Expense</button>
      </div>
    </form>
  </div>
</template>

<script setup>
const router = useRouter()
const config = useRuntimeConfig()
const { getAuthHeaders } = useAuth()

const form = ref({
  amount: '',
  description: '',
  category: 'Otros',
  transaction_type: 'expense',
  date: new Date().toISOString().split('T')[0]
})

const submitExpense = async () => {
  try {
    await $fetch('/api/expenses', {
      baseURL: config.public.apiUrl,
      method: 'POST',
      headers: getAuthHeaders(),
      body: form.value
    })
    router.push('/')
  } catch (error) {
    alert('Error adding expense: ' + error.message)
  }
}
</script>
