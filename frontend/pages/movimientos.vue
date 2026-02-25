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
        <USelect
          v-model="filters.month"
          :options="monthOptions"
          icon="i-heroicons-calendar"
          placeholder="Todos los meses"
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
        <UIcon name="i-heroicons-arrow-path" class="animate-spin text-3xl mb-3" />
        <p>Cargando transacciones...</p>
      </div>
      
      <!-- Error state -->
      <div v-else-if="loadError" class="p-8 text-center">
        <UIcon name="i-heroicons-exclamation-triangle" class="text-4xl text-red-300 dark:text-red-600 mb-3" />
        <p class="text-red-500 dark:text-red-400 mb-2">{{ loadError }}</p>
        <UButton 
          icon="i-heroicons-arrow-path" 
          color="primary" 
          variant="soft"
          @click="fetchTransactions"
        >
          Intentar de nuevo
        </UButton>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredTransactions.length === 0" class="p-8 text-center">
        <UIcon name="i-heroicons-inbox" class="text-4xl text-gray-300 dark:text-gray-600 mb-3" />
        <p class="text-gray-500 dark:text-gray-400 mb-2">No hay transacciones para mostrar</p>
        <p v-if="transactions.length === 0" class="text-sm text-gray-400 dark:text-gray-500 mb-4">
          Agrega tu primer movimiento haciendo clic en "Nuevo Movimiento"
        </p>
        <p v-else class="text-sm text-gray-400 dark:text-gray-500 mb-4">
          Prueba ajustando los filtros de busqueda
        </p>
        <UButton 
          icon="i-heroicons-arrow-path" 
          color="gray" 
          variant="soft"
          @click="fetchTransactions"
        >
          Recargar
        </UButton>
      </div>

      <!-- Mobile View: Card List (hidden on sm+) -->
      <div v-else-if="!loadError" class="sm:hidden divide-y divide-gray-100 dark:divide-gray-700">
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
              <!-- Mobile Actions -->
              <div class="flex items-center gap-2 mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
                <button 
                  @click.stop="openEditModal(t)"
                  class="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-primary dark:hover:text-primary transition-colors"
                >
                  <i class="fa-solid fa-pen-to-square"></i>
                  Editar
                </button>
                <button 
                  @click.stop="confirmDelete(t)"
                  class="flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 transition-colors"
                >
                  <i class="fa-solid fa-trash"></i>
                  Eliminar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop View: Table (hidden on mobile) -->
      <div v-if="!loading && !loadError && filteredTransactions.length > 0" class="hidden sm:block overflow-x-auto">
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
                <UButton icon="i-heroicons-pencil-square" color="gray" variant="ghost" size="xs" @click="openEditModal(t)" />
                <UButton icon="i-heroicons-trash" color="red" variant="ghost" size="xs" @click="confirmDelete(t)" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Modal -->
    <AddTransactionModal :is-open="showAddModal" @close="showAddModal = false" @saved="refreshData" />
    
    <!-- Edit Modal -->
    <EditTransactionModal 
      :is-open="showEditModal" 
      :transaction="selectedTransaction"
      @close="showEditModal = false" 
      @saved="refreshData" 
    />
    
    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="showDeleteModal" 
          class="fixed inset-0 z-50 flex items-end sm:items-center justify-center"
          @click.self="showDeleteModal = false"
        >
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-gray-900/70 backdrop-blur-sm" />
          
          <!-- Modal -->
          <Transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="transform translate-y-full sm:translate-y-4 sm:scale-95 opacity-0"
            enter-to-class="transform translate-y-0 sm:scale-100 opacity-100"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="transform translate-y-0 sm:scale-100 opacity-100"
            leave-to-class="transform translate-y-full sm:translate-y-4 sm:scale-95 opacity-0"
          >
            <div 
              v-if="showDeleteModal"
              class="relative w-full sm:w-[400px] bg-white dark:bg-gray-800 sm:rounded-2xl rounded-t-2xl shadow-2xl overflow-hidden"
            >
              <!-- Header -->
              <div class="px-4 sm:px-6 py-5 bg-red-500">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
                      <UIcon name="i-heroicons-trash" class="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h3 class="text-lg font-bold text-white">¿Eliminar?</h3>
                      <p class="text-red-100 text-sm">No se puede deshacer</p>
                    </div>
                  </div>
                  <button 
                    @click="showDeleteModal = false"
                    class="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center"
                  >
                    <UIcon name="i-heroicons-x-mark" class="w-5 h-5 text-white" />
                  </button>
                </div>
              </div>
              
              <!-- Content -->
              <div class="p-4 sm:p-6">
                <!-- Transaction Preview -->
                <div v-if="selectedTransaction" class="mb-5 bg-gray-50 dark:bg-gray-900/50 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
                  <div class="flex items-center gap-3">
                    <div 
                      class="w-12 h-12 rounded-xl flex items-center justify-center shrink-0"
                      :class="selectedTransaction.transaction_type == 'expense' 
                        ? 'bg-red-100 dark:bg-red-500/20 text-red-500' 
                        : 'bg-emerald-100 dark:bg-emerald-500/20 text-emerald-500'"
                    >
                      <UIcon :name="getCategoryIcon(selectedTransaction.category, selectedTransaction.transaction_type)" class="w-6 h-6" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="font-semibold text-gray-900 dark:text-white truncate">{{ selectedTransaction.description }}</p>
                      <p class="text-sm text-gray-500 dark:text-gray-400">{{ selectedTransaction.category }}</p>
                      <p class="text-xs text-gray-400 dark:text-gray-500">{{ formatDate(selectedTransaction.date) }}</p>
                    </div>
                    <div class="text-right">
                      <p 
                        class="text-lg font-bold"
                        :class="selectedTransaction.transaction_type == 'expense' ? 'text-red-500' : 'text-emerald-500'"
                      >
                        {{ selectedTransaction.transaction_type == 'expense' ? '-' : '+' }}${{ formatNumber(selectedTransaction.amount) }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <!-- Actions -->
                <div class="flex gap-3">
                  <button 
                    @click="showDeleteModal = false"
                    class="flex-1 px-4 py-3.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-xl active:scale-95 transition-transform"
                    :disabled="isDeleting"
                  >
                    Cancelar
                  </button>
                  <button 
                    @click="deleteTransaction()"
                    :disabled="isDeleting"
                    class="flex-1 px-4 py-3.5 bg-red-500 text-white font-semibold rounded-xl active:scale-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    <UIcon v-if="isDeleting" name="i-heroicons-arrow-path" class="w-5 h-5 animate-spin" />
                    <span v-else>Eliminar</span>
                  </button>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import AddTransactionModal from '~/components/AddTransactionModal.vue'
import EditTransactionModal from '~/components/EditTransactionModal.vue'

definePageMeta({
  layout: 'default',
  middleware: 'auth',
  title: 'Movements'
})

const { getAuthHeaders, token } = useAuth()
const { success: notifySuccess, error: notifyError } = useNotification()
const config = useRuntimeConfig()

// State
const loading = ref(true)
const loadError = ref('')
const transactions = ref<any[]>([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const selectedTransaction = ref<any>(null)
const isDeleting = ref(false)

// Filters State
const filters = reactive({
  search: '',
  month: '' // Empty by default to show all transactions
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

// Generate month options for filter
const monthOptions = computed(() => {
  const options = [{ label: 'Todos los meses', value: '' }]
  const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  
  // Get unique months from transactions
  const uniqueMonths = new Set<string>()
  transactions.value.forEach(t => {
    if (t.date) {
      const d = new Date(t.date)
      const monthKey = `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}`
      uniqueMonths.add(monthKey)
    }
  })
  
  // Sort and format
  Array.from(uniqueMonths).sort().reverse().forEach(key => {
    const [year, month] = key.split('-')
    options.push({
      label: `${months[parseInt(month) - 1]} ${year}`,
      value: key
    })
  })
  
  return options
})

// Fetch Data
const fetchTransactions = async () => {
  loading.value = true
  loadError.value = ''
  
  try {
    console.log('Fetching transactions...')
    
    if (!token.value) {
      console.log('No token available, waiting...')
      loadError.value = 'No hay sesion activa. Por favor inicia sesion.'
      return
    }
    
    const response = await $fetch('/api/expenses/all', {
      baseURL: config.public.apiUrl,
      headers: getAuthHeaders(),
      params: { limit: 500 }
    })
    
    console.log('Response:', response)
    
    if (Array.isArray(response)) {
      transactions.value = response
      console.log(`Loaded ${response.length} transactions`)
    } else {
      console.error('Invalid response format:', response)
      transactions.value = []
      loadError.value = 'Formato de respuesta invalido'
    }
  } catch (e: any) {
    console.error('Error fetching transactions:', e)
    loadError.value = e?.data?.detail || 'Error al cargar los movimientos. Intenta de nuevo.'
    // Error shown in UI
    transactions.value = []
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
      if (!t.date) return false
      const d = new Date(t.date)
      // Use UTC methods to avoid timezone issues
      return d.getUTCFullYear() === parseInt(year) && (d.getUTCMonth() + 1) === parseInt(month)
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
const formatDate = (d: string | Date) => {
  if (!d) return ''
  const date = new Date(d)
  return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric', year: 'numeric' })
}
const resetFilters = () => {
  filters.search = ''
  filters.month = ''
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

// Edit & Delete Functions
const openEditModal = (transaction: any) => {
  selectedTransaction.value = transaction
  showEditModal.value = true
}

const confirmDelete = (transaction: any) => {
  selectedTransaction.value = transaction
  showDeleteModal.value = true
}

const deleteTransaction = async () => {
  if (!selectedTransaction.value) return
  
  isDeleting.value = true
  try {
    await $fetch(`/api/expenses/${selectedTransaction.value.id}`, {
      baseURL: config.public.apiUrl,
      method: 'DELETE',
      headers: getAuthHeaders()
    })
    
    showDeleteModal.value = false
    notifySuccess('Movimiento eliminado', 'El movimiento se eliminó correctamente')
    await refreshData()
  } catch (e: any) {
    console.error('Error deleting transaction:', e)
    notifyError('Error', e?.data?.detail || 'No se pudo eliminar el movimiento')
  } finally {
    isDeleting.value = false
    selectedTransaction.value = null
  }
}

// Init
onMounted(async () => {
  console.log('Movimientos page mounted')
  // Wait a bit for auth to initialize
  await nextTick()
  
  // Try to fetch if we have token, otherwise wait for auth init
  if (token.value) {
    await fetchTransactions()
  } else {
    // Wait for auth initialization (max 3 seconds)
    let attempts = 0
    const maxAttempts = 30
    
    while (!token.value && attempts < maxAttempts) {
      await new Promise(r => setTimeout(r, 100))
      attempts++
    }
    
    if (token.value) {
      await fetchTransactions()
    } else {
      console.log('No token available after waiting')
      loading.value = false
    }
  }
})
</script>
