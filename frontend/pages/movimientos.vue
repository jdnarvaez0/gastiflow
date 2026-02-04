<template>
  <div class="space-y-4 sm:space-y-6 w-full max-w-full overflow-x-hidden">
    <!-- Page Header -->
    <div class="flex flex-col gap-3 sm:gap-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold font-display text-gray-900 dark:text-white">{{ $t('nav.movements') }}</h1>
        <p class="text-gray-500 dark:text-gray-400 text-xs sm:text-sm">Manage and track all your transactions.</p>
      </div>
      <div class="flex gap-2 w-full sm:w-auto">
        <UButton 
          icon="i-heroicons-arrow-down-tray" 
          color="gray" 
          variant="soft"
          @click="exportToCSV"
        >
          Export CSV
        </UButton>
        <UButton 
          icon="i-heroicons-plus" 
          color="primary" 
          class="shadow-lg shadow-primary/30"
          @click="showAddModal = true"
        >
          {{ $t('dashboard.newMovement') }}
        </UButton>
      </div>
    </div>

    <!-- Summary Cards (Dynamic based on filtered data) -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
      <div class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm relative overflow-hidden group">
        <div class="relative z-10">
          <p class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">Total Income</p>
          <div class="text-xl sm:text-2xl font-bold text-emerald-500">+${{ formatNumber(summary.income) }}</div>
        </div>
        <UIcon name="i-heroicons-arrow-trending-up" class="absolute right-2 top-2 w-10 h-10 sm:w-12 sm:h-12 text-emerald-500/10 group-hover:scale-110 transition-transform" />
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm relative overflow-hidden group">
        <div class="relative z-10">
          <p class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">Total Expenses</p>
          <div class="text-xl sm:text-2xl font-bold text-red-500">-${{ formatNumber(summary.expenses) }}</div>
        </div>
        <UIcon name="i-heroicons-arrow-trending-down" class="absolute right-2 top-2 w-10 h-10 sm:w-12 sm:h-12 text-red-500/10 group-hover:scale-110 transition-transform" />
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm relative overflow-hidden group">
        <div class="relative z-10">
          <p class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">Net Balance</p>
          <div class="text-xl sm:text-2xl font-bold text-primary">${{ formatNumber(summary.balance) }}</div>
        </div>
        <UIcon name="i-heroicons-scale" class="absolute right-2 top-2 w-10 h-10 sm:w-12 sm:h-12 text-primary/10 group-hover:scale-110 transition-transform" />
      </div>
    </div>

    <!-- Filters & Search -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-3 sm:p-4 border border-gray-200 dark:border-gray-700 shadow-sm">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <!-- Search -->
        <UInput 
          v-model="filters.search"
          icon="i-heroicons-magnifying-glass" 
          placeholder="Buscar descripción, categoría o tipo..." 
          variant="outline"
          class="sm:col-span-2"
          :ui="{ icon: { trailing: { pointer: '' } } }"
        />
        
        <!-- Date Filter (Month) -->
        <UInput 
          v-model="filters.month"
          type="month"
          icon="i-heroicons-calendar"
          placeholder="Seleccionar Mes"
          class="w-full"
          variant="outline"
        />
        
        <!-- Clear Filters -->
        <UButton icon="i-heroicons-x-mark" color="gray" variant="ghost" @click="resetFilters" class="lg:hidden">Clear</UButton>
      </div>
    </div>

    <!-- Transactions List -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <!-- Loading state -->
      <div v-if="loading" class="p-8 text-center text-gray-500 dark:text-gray-400">
        <i class="fa-solid fa-spinner fa-spin text-2xl mb-2"></i>
        <p>Cargando transacciones...</p>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredTransactions.length === 0" class="p-8 text-center">
        <i class="fa-solid fa-inbox text-4xl text-gray-300 dark:text-gray-600 mb-3"></i>
        <p class="text-gray-500 dark:text-gray-400">No hay transacciones para mostrar</p>
      </div>

      <!-- Mobile View: Card List (hidden on sm+) -->
      <div v-else class="sm:hidden divide-y divide-gray-100 dark:divide-gray-700">
        <div 
          v-for="t in filteredTransactions" 
          :key="t.id" 
          class="p-4 hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors active:bg-gray-100 dark:active:bg-gray-700/50"
        >
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div 
              class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
              :class="t.transaction_type == 'expense' 
                ? 'bg-red-100 dark:bg-red-500/20 text-red-500' 
                : 'bg-emerald-100 dark:bg-emerald-500/20 text-emerald-500'"
            >
              <UIcon :name="getCategoryIcon(t.category, t.transaction_type)" class="w-5 h-5" />
            </div>
            
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <div class="min-w-0">
                  <p class="font-semibold text-gray-900 dark:text-white text-sm truncate">{{ t.description }}</p>
                  <div class="flex items-center gap-2 mt-0.5">
                    <span class="text-xs text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full">{{ t.category }}</span>
                  </div>
                </div>
                <div class="text-right shrink-0">
                  <p 
                    class="font-bold text-sm"
                    :class="t.transaction_type == 'expense' ? 'text-red-500' : 'text-emerald-500'"
                  >
                    {{ t.transaction_type == 'expense' ? '-' : '+' }}${{ formatNumber(t.amount) }}
                  </p>
                  <p class="text-xs text-gray-400 dark:text-gray-500 mt-0.5">{{ formatDate(t.date) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop View: Table (hidden on mobile) -->
      <div v-if="!loading && filteredTransactions.length > 0" class="hidden sm:block overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700/50 border-b border-gray-200 dark:border-gray-700">
              <th @click="toggleSort('description')" class="text-left py-4 px-6 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors">
                Transaction
                <UIcon v-if="sort.column === 'description'" :name="sort.direction === 'asc' ? 'i-heroicons-bars-arrow-up' : 'i-heroicons-bars-arrow-down'" class="ml-1 w-3 h-3 text-primary" />
              </th>
              <th @click="toggleSort('category')" class="text-left py-4 px-6 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors">
                Category
                <UIcon v-if="sort.column === 'category'" :name="sort.direction === 'asc' ? 'i-heroicons-bars-arrow-up' : 'i-heroicons-bars-arrow-down'" class="ml-1 w-3 h-3 text-primary" />
              </th>
              <th @click="toggleSort('date')" class="text-left py-4 px-6 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider hidden md:table-cell cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors">
                Date
                <UIcon v-if="sort.column === 'date'" :name="sort.direction === 'asc' ? 'i-heroicons-bars-arrow-up' : 'i-heroicons-bars-arrow-down'" class="ml-1 w-3 h-3 text-primary" />
              </th>
              <th @click="toggleSort('amount')" class="text-right py-4 px-6 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors">
                Amount
                <UIcon v-if="sort.column === 'amount'" :name="sort.direction === 'asc' ? 'i-heroicons-bars-arrow-up' : 'i-heroicons-bars-arrow-down'" class="ml-1 w-3 h-3 text-primary" />
              </th>
              <th class="text-right py-4 px-6 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider hidden lg:table-cell">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr v-for="t in filteredTransactions" :key="t.id" class="group hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
              <td class="py-4 px-6">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                    :class="t.transaction_type == 'expense' 
                      ? 'bg-red-100 dark:bg-red-500/20 text-red-500' 
                      : 'bg-emerald-100 dark:bg-emerald-500/20 text-emerald-500'">
                    <UIcon :name="getCategoryIcon(t.category, t.transaction_type)" class="w-5 h-5" />
                  </div>
                  <div class="font-semibold text-gray-900 dark:text-white text-sm">{{ t.description }}</div>
                </div>
              </td>
              <td class="py-4 px-6 text-sm text-gray-600 dark:text-gray-400">
                <UBadge color="gray" variant="soft" size="sm">{{ t.category }}</UBadge>
              </td>
              <td class="py-4 px-6 text-sm text-gray-500 dark:text-gray-400 hidden md:table-cell">
                {{ formatDate(t.date) }}
              </td>
              <td class="py-4 px-6 text-right font-bold text-sm whitespace-nowrap" 
                 :class="t.transaction_type == 'expense' ? 'text-gray-900 dark:text-white' : 'text-emerald-500'">
                 {{ t.transaction_type == 'expense' ? '-' : '+' }}${{ formatNumber(t.amount) }}
              </td>
              <td class="py-4 px-6 text-right hidden lg:table-cell opacity-0 group-hover:opacity-100 transition-opacity">
                <UButton icon="i-heroicons-pencil-square" color="gray" variant="ghost" size="xs" />
                <UButton icon="i-heroicons-trash" color="red" variant="ghost" size="xs" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Modal -->
    <AddTransactionModal :is-open="showAddModal" @close="showAddModal = false" @saved="refreshData" />
  </div>
</template>

<script setup lang="ts">
import AddTransactionModal from '~/components/AddTransactionModal.vue'

definePageMeta({
  layout: 'default',
  middleware: 'auth',
  title: 'Movements'
})

const { getAuthHeaders, token } = useAuth()
const config = useRuntimeConfig()

// State
const loading = ref(true)
const transactions = ref<any[]>([])
const showAddModal = ref(false)

// Filters State
const filters = reactive({
  search: '',
  month: new Date().toISOString().slice(0, 7) // Default to current month YYYY-MM
})

// Sorting State
const sort = reactive({
  column: 'date',
  direction: 'desc' as 'asc' | 'desc'
})

// Categories List (Matched with Backend Enum)
const categories = [
  'Supermercado', 'Transporte', 'Restaurante', 'Entretenimiento', 'Salud', 
  'Servicios', 'Educación', 'Ropa', 'Tecnología', 'Otros', 
  'Comida', 'Hogar', 'Viajes', 'Gasolina', 'Deportes', 'Mascotas', 
  'Regalos', 'Salario', 'Freelance', 'Ventas', 'Inversiones'
].sort()

// Fetch Data
const fetchTransactions = async () => {
  loading.value = true
  try {
    const response = await $fetch<any[]>('/api/expenses', {
      baseURL: config.public.apiUrl,
      headers: getAuthHeaders(),
      params: { limit: 1000 }
    })
    transactions.value = response
  } catch (e) {
    console.error('Error fetching transactions', e)
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
    await fetchTransactions()
}

// Toggle Sort
const toggleSort = (column: string) => {
  if (sort.column === column) {
    sort.direction = sort.direction === 'asc' ? 'desc' : 'asc'
  } else {
    sort.column = column
    sort.direction = 'desc'
  }
}

// Computed: Filtered & Sorted Transactions
const filteredTransactions = computed(() => {
  let result = [...transactions.value]

  // Search
  if (filters.search) {
    const q = filters.search.toLowerCase()
    result = result.filter(t => 
      t.description.toLowerCase().includes(q) || 
      t.category?.toLowerCase().includes(q) ||
      (t.transaction_type === 'expense' && 'gasto'.includes(q)) ||
      (t.transaction_type === 'income' && 'ingreso'.includes(q))
    )
  }
  
  // Date Filter (Month)
  if (filters.month) {
      const [year, month] = filters.month.split('-')
      result = result.filter(t => {
          const d = new Date(t.date)
          return d.getFullYear() === parseInt(year) && (d.getMonth() + 1) === parseInt(month)
      })
  }


  // Sort
  result.sort((a, b) => {
    let valA = a[sort.column]
    let valB = b[sort.column]

    // Handle dates
    if (sort.column === 'date') {
        valA = new Date(valA).getTime()
        valB = new Date(valB).getTime()
    }

    if (valA < valB) return sort.direction === 'asc' ? -1 : 1
    if (valA > valB) return sort.direction === 'asc' ? 1 : -1
    return 0
  })

  return result
})

// Computed: Summary Stats based on filtered view
const summary = computed(() => {
  const data = filteredTransactions.value
  const income = data.filter(t => t.transaction_type === 'income').reduce((sum, t) => sum + t.amount, 0)
  const expenses = data.filter(t => t.transaction_type === 'expense').reduce((sum, t) => sum + t.amount, 0)
  return {
    income,
    expenses,
    balance: income - expenses
  }
})

// Helpers
const formatNumber = (num: number) => new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num || 0)
const formatDate = (d: string) => new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const resetFilters = () => {
  filters.search = ''
  filters.month = new Date().toISOString().slice(0, 7)
}

const getCategoryIcon = (category: string, type: string) => {
    if (type === 'income') return 'i-heroicons-banknotes';
    
    // Normalize category key for lookup (title case)
    const normCat = categories.find(c => c.toLowerCase() === category?.toLowerCase()) || category;
    
    const iconMap: Record<string, string> = {
        'Transporte': 'i-heroicons-truck',
        'Supermercado': 'i-heroicons-shopping-cart',
        'Restaurante': 'i-heroicons-cake',
        'Comida': 'i-heroicons-cake',
        'Hogar': 'i-heroicons-home',
        'Servicios': 'i-heroicons-bolt',
        'Salud': 'i-heroicons-heart',
        'Entretenimiento': 'i-heroicons-ticket',
        'Educación': 'i-heroicons-academic-cap',
        'Ropa': 'i-heroicons-shopping-bag',
        'Viajes': 'i-heroicons-paper-airplane',
        'Gasolina': 'i-heroicons-fire',
        'Deportes': 'i-heroicons-trophy',
        'Mascotas': 'i-heroicons-face-smile',
        'Tecnología': 'i-heroicons-computer-desktop',
        'Regalos': 'i-heroicons-gift',
        'Salario': 'i-heroicons-banknotes',
        'Freelance': 'i-heroicons-briefcase',
        'Ventas': 'i-heroicons-currency-dollar',
        'Inversiones': 'i-heroicons-chart-bar',
        'Otros': 'i-heroicons-tag'
    };
    return iconMap[normCat] || 'i-heroicons-tag';
}

// Export CSV
const exportToCSV = () => {
    const headers = ['Date', 'Description', 'Category', 'Type', 'Amount']
    const rows = filteredTransactions.value.map(t => [
        new Date(t.date).toLocaleDateString(),
        `"${t.description}"`, // Quote strings to handle commas
        t.category,
        t.transaction_type,
        t.amount
    ])
    
    const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `gastiflow_export_${new Date().toISOString().split('T')[0]}.csv`
    link.click()
}

// Init
onMounted(() => {
  if (token.value) fetchTransactions()
})
</script>
