<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6">Gastiflow Dashboard</h1>

    <div v-if="pending" class="text-center">Loading...</div>
    <div v-else-if="error" class="text-red-500">Error loading data: {{ error.message }}</div>
    <div v-else>
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-gray-500 text-sm">Income</h3>
          <p class="text-2xl font-bold text-green-600">${{ data.stats.income }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-gray-500 text-sm">Expenses</h3>
          <p class="text-2xl font-bold text-red-600">${{ data.stats.expenses }}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-gray-500 text-sm">Balance</h3>
          <p class="text-2xl font-bold" :class="data.stats.balance >= 0 ? 'text-green-600' : 'text-red-600'">
            ${{ data.stats.balance }}
          </p>
        </div>
      </div>

      <!-- Recent Expenses -->
      <div class="bg-white rounded-lg shadow overflow-hidden mb-8">
        <div class="px-6 py-4 border-b flex justify-between items-center">
          <h2 class="text-xl font-semibold">Recent Expenses</h2>
          <NuxtLink to="/add" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
            Add Expense
          </NuxtLink>
        </div>
        <table class="min-w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="expense in data.expenses" :key="expense.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ new Date(expense.date).toLocaleDateString() }}</td>
              <td class="px-6 py-4">{{ expense.description }}</td>
              <td class="px-6 py-4">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                  {{ expense.category }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap" :class="expense.transaction_type === 'income' ? 'text-green-600' : 'text-red-600'">
                {{ expense.transaction_type === 'income' ? '+' : '-' }}${{ expense.amount }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const { data, pending, error } = await useFetch('/api/dashboard')
</script>
