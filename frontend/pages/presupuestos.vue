<template>
  <div class="space-y-4 sm:space-y-6 w-full max-w-full overflow-x-hidden">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">Presupuestos</h1>
        <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">Controla tus gastos por categoría</p>
      </div>
      <button 
        @click="openAddModal"
        class="px-4 py-2.5 bg-primary text-white rounded-xl font-medium hover:bg-primary-dark transition-colors flex items-center justify-center gap-2 shadow-lg shadow-primary/30"
      >
        <UIcon name="i-heroicons-plus" class="w-5 h-5" />
        <span>Nuevo Presupuesto</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-primary" />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <UIcon name="i-heroicons-exclamation-circle" class="w-12 h-12 text-red-500 mx-auto mb-3" />
      <p class="text-red-500">{{ error }}</p>
      <button @click="fetchBudgets" class="mt-3 text-primary hover:underline">Reintentar</button>
    </div>

    <template v-else>
      <!-- Resumen General -->
      <div v-if="budgets.length > 0" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 shadow-sm">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <UIcon name="i-heroicons-wallet" class="w-5 h-5 text-primary" />
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Presupuesto Total</span>
          </div>
          <p class="text-2xl font-bold text-gray-900 dark:text-white">${{ formatNumber(totalBudget) }}</p>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 shadow-sm">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
              <UIcon name="i-heroicons-arrow-trending-down" class="w-5 h-5 text-red-500" />
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Gastado</span>
          </div>
          <p class="text-2xl font-bold text-red-500">${{ formatNumber(totalSpent) }}</p>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 shadow-sm">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
              <UIcon name="i-heroicons-banknotes" class="w-5 h-5 text-emerald-500" />
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Restante</span>
          </div>
          <p class="text-2xl font-bold" :class="totalRemaining >= 0 ? 'text-emerald-500' : 'text-red-500'">
            ${{ formatNumber(totalRemaining) }}
          </p>
        </div>
      </div>

      <!-- Alertas -->
      <div v-if="alerts.length > 0" class="space-y-2">
        <div 
          v-for="alert in alerts" 
          :key="alert.budget_id"
          class="flex items-center gap-3 p-4 rounded-xl border"
          :class="alert.severity === 'danger' 
            ? 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800' 
            : 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800'"
        >
          <UIcon 
            :name="alert.severity === 'danger' ? 'i-heroicons-exclamation-circle' : 'i-heroicons-exclamation-triangle'"
            class="w-6 h-6 flex-shrink-0"
            :class="alert.severity === 'danger' ? 'text-red-500' : 'text-amber-500'"
          />
          <div class="flex-1">
            <p class="font-medium text-sm" :class="alert.severity === 'danger' ? 'text-red-700 dark:text-red-400' : 'text-amber-700 dark:text-amber-400'">
              {{ alert.message }}
            </p>
            <p class="text-xs mt-0.5" :class="alert.severity === 'danger' ? 'text-red-600/70 dark:text-red-400/70' : 'text-amber-600/70 dark:text-amber-400/70'">
              ${{ formatNumber(alert.spent) }} de ${{ formatNumber(alert.budget_amount) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Lista de Presupuestos -->
      <div v-if="budgets.length === 0" class="text-center py-12 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
        <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center mx-auto mb-4">
          <UIcon name="i-heroicons-wallet" class="w-8 h-8 text-gray-400" />
        </div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">No tienes presupuestos</h3>
        <p class="text-gray-500 dark:text-gray-400 text-sm mb-4 max-w-sm mx-auto">
          Crea presupuestos por categoría para controlar tus gastos y recibir alertas
        </p>
        <button 
          @click="openAddModal"
          class="px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark transition-colors"
        >
          Crear mi primer presupuesto
        </button>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div 
          v-for="budget in budgets" 
          :key="budget.id"
          class="bg-white dark:bg-gray-800 rounded-xl p-4 sm:p-5 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center gap-3">
              <div 
                class="w-10 h-10 rounded-xl flex items-center justify-center"
                :class="getCategoryColor(budget.category)"
              >
                <UIcon :name="getCategoryIcon(budget.category)" class="w-5 h-5" />
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white">{{ budget.category }}</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400">Límite: ${{ formatNumber(budget.amount) }}/mes</p>
              </div>
            </div>
            <div class="flex items-center gap-1">
              <button 
                @click="openEditModal(budget)"
                class="w-8 h-8 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center justify-center text-gray-500 transition-colors"
              >
                <UIcon name="i-heroicons-pencil" class="w-4 h-4" />
              </button>
              <button 
                @click="confirmDelete(budget)"
                class="w-8 h-8 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/30 flex items-center justify-center text-gray-500 hover:text-red-500 transition-colors"
              >
                <UIcon name="i-heroicons-trash" class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Progress Bar -->
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="font-medium" :class="getProgressColor(budget.percentage_used)">
                {{ budget.percentage_used.toFixed(0) }}%
              </span>
              <span class="text-gray-500 dark:text-gray-400">
                ${{ formatNumber(budget.spent) }} / ${{ formatNumber(budget.amount) }}
              </span>
            </div>
            <div class="h-3 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
              <div 
                class="h-full rounded-full transition-all duration-500"
                :class="getProgressBarColor(budget.percentage_used)"
                :style="{ width: Math.min(budget.percentage_used, 100) + '%' }"
              />
            </div>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-500 dark:text-gray-400">
                Restante: ${{ formatNumber(budget.remaining) }}
              </span>
              <span 
                v-if="budget.alert_triggered"
                class="flex items-center gap-1 font-medium"
                :class="budget.percentage_used >= 100 ? 'text-red-500' : 'text-amber-500'"
              >
                <UIcon 
                  :name="budget.percentage_used >= 100 ? 'i-heroicons-exclamation-circle' : 'i-heroicons-exclamation-triangle'" 
                  class="w-3.5 h-3.5" 
                />
                {{ budget.percentage_used >= 100 ? 'Excedido' : 'Alerta' }}
              </span>
              <span v-else class="text-emerald-500 flex items-center gap-1">
                <UIcon name="i-heroicons-check-circle" class="w-3.5 h-3.5" />
                En orden
              </span>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Modal para Crear/Editar -->
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
          v-if="showModal" 
          class="fixed inset-0 z-50 flex items-end sm:items-center justify-center"
          @click.self="closeModal"
        >
          <div class="absolute inset-0 bg-gray-900/70 backdrop-blur-sm" />
          
          <Transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="transform translate-y-full sm:translate-y-4 sm:scale-95 opacity-0"
            enter-to-class="transform translate-y-0 sm:scale-100 opacity-100"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="transform translate-y-0 sm:scale-100 opacity-100"
            leave-to-class="transform translate-y-full sm:translate-y-4 sm:scale-95 opacity-0"
          >
            <div 
              v-if="showModal"
              class="relative w-full sm:w-[480px] max-h-[90vh] sm:max-h-[85vh] bg-white dark:bg-gray-800 sm:rounded-2xl rounded-t-2xl shadow-2xl overflow-hidden flex flex-col"
            >
              <!-- Header -->
              <div class="flex-shrink-0 px-4 sm:px-6 py-4 bg-primary">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
                      <UIcon :name="editingBudget ? 'i-heroicons-pencil-square' : 'i-heroicons-plus-circle'" class="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h3 class="text-lg font-bold text-white">
                        {{ editingBudget ? 'Editar Presupuesto' : 'Nuevo Presupuesto' }}
                      </h3>
                    </div>
                  </div>
                  <button 
                    @click="closeModal"
                    class="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center"
                  >
                    <UIcon name="i-heroicons-x-mark" class="w-5 h-5 text-white" />
                  </button>
                </div>
              </div>

              <!-- Content -->
              <div class="flex-1 overflow-y-auto overscroll-contain">
                <div class="p-4 sm:p-6 space-y-5">
                  <!-- Error -->
                  <div v-if="modalError" class="flex items-start gap-2 px-4 py-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400 text-sm">
                    <UIcon name="i-heroicons-exclamation-circle" class="w-5 h-5 flex-shrink-0" />
                    <span>{{ modalError }}</span>
                  </div>

                  <!-- Categoría -->
                  <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                      Categoría
                    </label>
                    <div class="grid grid-cols-3 gap-2">
                      <button
                        v-for="cat in availableCategories"
                        :key="cat.value"
                        type="button"
                        @click="form.category = cat.value"
                        class="flex flex-col items-center gap-1.5 p-3 rounded-xl border-2 transition-all min-h-[72px] justify-center"
                        :class="form.category === cat.value 
                          ? 'border-primary bg-primary/10 text-primary' 
                          : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400'"
                      >
                        <UIcon :name="cat.icon" class="w-5 h-5" />
                        <span class="text-xs font-medium">{{ cat.label }}</span>
                      </button>
                    </div>
                  </div>

                  <!-- Monto -->
                  <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                      Monto mensual
                    </label>
                    <div class="relative">
                      <span class="absolute left-4 top-1/2 -translate-y-1/2 text-xl font-bold text-primary">$</span>
                      <input 
                        v-model.number="form.amount" 
                        type="number" 
                        step="1000"
                        inputmode="numeric"
                        required 
                        placeholder="500000"
                        class="w-full pl-10 pr-4 py-4 text-2xl font-bold bg-gray-50 dark:bg-gray-900 border-2 border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-white focus:outline-none focus:border-primary transition-colors"
                      />
                    </div>
                  </div>

                  <!-- Alerta -->
                  <div>
                    <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                      Alertar al alcanzar
                    </label>
                    <div class="flex gap-2">
                      <button
                        v-for="threshold in [70, 80, 90]"
                        :key="threshold"
                        type="button"
                        @click="form.alert_threshold = threshold / 100"
                        class="flex-1 py-3 px-4 rounded-xl border-2 font-medium transition-all"
                        :class="form.alert_threshold === threshold / 100 
                          ? 'border-amber-500 bg-amber-50 dark:bg-amber-900/20 text-amber-600' 
                          : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400'"
                      >
                        {{ threshold }}%
                      </button>
                    </div>
                    <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
                      Te notificaremos cuando hayas gastado este porcentaje de tu presupuesto
                    </p>
                  </div>
                </div>
              </div>

              <!-- Footer -->
              <div class="flex-shrink-0 p-4 sm:p-6 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <div class="flex gap-3">
                  <button 
                    type="button"
                    @click="closeModal"
                    class="flex-1 px-4 py-3.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-xl active:scale-95 transition-transform"
                  >
                    Cancelar
                  </button>
                  <button 
                    type="button"
                    @click="saveBudget"
                    class="flex-1 px-4 py-3.5 bg-primary text-white font-semibold rounded-xl active:scale-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                    :disabled="saving || !isFormValid"
                  >
                    <UIcon v-if="saving" name="i-heroicons-arrow-path" class="w-5 h-5 animate-spin" />
                    <span v-else>{{ editingBudget ? 'Guardar' : 'Crear' }}</span>
                  </button>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>

    <!-- Modal de Confirmar Eliminación -->
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
          <div class="absolute inset-0 bg-gray-900/70 backdrop-blur-sm" />
          
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
              <div class="px-4 sm:px-6 py-5 bg-red-500">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
                      <UIcon name="i-heroicons-trash" class="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h3 class="text-lg font-bold text-white">¿Eliminar?</h3>
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

              <div class="p-4 sm:p-6">
                <p class="text-gray-600 dark:text-gray-400 mb-5">
                  ¿Estás seguro de eliminar el presupuesto de <strong class="text-gray-900 dark:text-white">{{ budgetToDelete?.category }}</strong>?
                </p>

                <div class="flex gap-3">
                  <button 
                    @click="showDeleteModal = false"
                    class="flex-1 px-4 py-3.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-xl active:scale-95 transition-transform"
                  >
                    Cancelar
                  </button>
                  <button 
                    @click="deleteBudget"
                    class="flex-1 px-4 py-3.5 bg-red-500 text-white font-semibold rounded-xl active:scale-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                    :disabled="deleting"
                  >
                    <UIcon v-if="deleting" name="i-heroicons-arrow-path" class="w-5 h-5 animate-spin" />
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

<script setup>
definePageMeta({
  layout: 'default',
  middleware: 'auth',
  title: 'Presupuestos'
})

const config = useRuntimeConfig()
const { getAuthHeaders } = useAuth()
const { success: notifySuccess, error: notifyError } = useNotification()

// State
const loading = ref(true)
const error = ref('')
const budgets = ref([])
const alerts = ref([])

// Modal state
const showModal = ref(false)
const showDeleteModal = ref(false)
const editingBudget = ref(null)
const budgetToDelete = ref(null)
const saving = ref(false)
const deleting = ref(false)
const modalError = ref('')

const form = reactive({
  category: 'Comida',
  amount: '',
  alert_threshold: 0.8
})

// Categorías disponibles (sin presupuesto actual)
const expenseCategories = [
  { value: 'Comida', label: 'Comida', icon: 'i-heroicons-cake' },
  { value: 'Transporte', label: 'Transporte', icon: 'i-heroicons-truck' },
  { value: 'Hogar', label: 'Hogar', icon: 'i-heroicons-home' },
  { value: 'Servicios', label: 'Servicios', icon: 'i-heroicons-bolt' },
  { value: 'Entretenimiento', label: 'Entretenimiento', icon: 'i-heroicons-ticket' },
  { value: 'Salud', label: 'Salud', icon: 'i-heroicons-heart' },
  { value: 'Educación', label: 'Educación', icon: 'i-heroicons-academic-cap' },
  { value: 'Ropa', label: 'Ropa', icon: 'i-heroicons-shopping-bag' },
  { value: 'Viajes', label: 'Viajes', icon: 'i-heroicons-paper-airplane' },
  { value: 'Gasolina', label: 'Gasolina', icon: 'i-heroicons-fire' },
  { value: 'Deportes', label: 'Deportes', icon: 'i-heroicons-trophy' },
  { value: 'Mascotas', label: 'Mascotas', icon: 'i-heroicons-face-smile' },
  { value: 'Tecnología', label: 'Tecnología', icon: 'i-heroicons-computer-desktop' },
  { value: 'Regalos', label: 'Regalos', icon: 'i-heroicons-gift' },
  { value: 'Otros', label: 'Otros', icon: 'i-heroicons-tag' },
]

const availableCategories = computed(() => {
  if (editingBudget.value) {
    return expenseCategories
  }
  const usedCategories = budgets.value.map(b => b.category)
  return expenseCategories.filter(cat => !usedCategories.includes(cat.value))
})

const isFormValid = computed(() => {
  return form.category && form.amount && form.amount > 0
})

// Computed
const totalBudget = computed(() => budgets.value.reduce((sum, b) => sum + b.amount, 0))
const totalSpent = computed(() => budgets.value.reduce((sum, b) => sum + b.spent, 0))
const totalRemaining = computed(() => totalBudget.value - totalSpent.value)

// Methods
const formatNumber = (num) => {
  if (!num && num !== 0) return '0'
  return new Intl.NumberFormat('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(num)
}

const getCategoryIcon = (category) => {
  const cat = expenseCategories.find(c => c.value === category)
  return cat?.icon || 'i-heroicons-tag'
}

const getCategoryColor = (category) => {
  const colors = {
    'Comida': 'bg-orange-100 text-orange-600',
    'Transporte': 'bg-blue-100 text-blue-600',
    'Hogar': 'bg-emerald-100 text-emerald-600',
    'Servicios': 'bg-yellow-100 text-yellow-600',
    'Entretenimiento': 'bg-purple-100 text-purple-600',
    'Salud': 'bg-red-100 text-red-600',
    'Educación': 'bg-indigo-100 text-indigo-600',
    'Ropa': 'bg-pink-100 text-pink-600',
    'Viajes': 'bg-cyan-100 text-cyan-600',
    'Gasolina': 'bg-amber-100 text-amber-600',
    'Deportes': 'bg-lime-100 text-lime-600',
    'Mascotas': 'bg-teal-100 text-teal-600',
    'Tecnología': 'bg-gray-100 text-gray-600',
    'Regalos': 'bg-rose-100 text-rose-600',
    'Otros': 'bg-slate-100 text-slate-600',
  }
  return colors[category] || 'bg-gray-100 text-gray-600'
}

const getProgressColor = (percentage) => {
  if (percentage >= 100) return 'text-red-500'
  if (percentage >= 80) return 'text-amber-500'
  return 'text-emerald-500'
}

const getProgressBarColor = (percentage) => {
  if (percentage >= 100) return 'bg-red-500'
  if (percentage >= 80) return 'bg-amber-500'
  return 'bg-emerald-500'
}

const fetchBudgets = async () => {
  loading.value = true
  error.value = ''
  try {
    const [budgetsData, alertsData] = await Promise.all([
      $fetch('/api/budgets', {
        baseURL: config.public.apiUrl,
        headers: getAuthHeaders()
      }),
      $fetch('/api/budgets/alerts', {
        baseURL: config.public.apiUrl,
        headers: getAuthHeaders()
      })
    ])
    budgets.value = budgetsData
    alerts.value = alertsData
  } catch (e) {
    console.error('Error fetching budgets:', e)
    error.value = 'Error al cargar los presupuestos'
  } finally {
    loading.value = false
  }
}

const openAddModal = () => {
  editingBudget.value = null
  form.category = availableCategories.value[0]?.value || 'Comida'
  form.amount = ''
  form.alert_threshold = 0.8
  modalError.value = ''
  showModal.value = true
}

const openEditModal = (budget) => {
  editingBudget.value = budget
  form.category = budget.category
  form.amount = budget.amount
  form.alert_threshold = budget.alert_threshold
  modalError.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingBudget.value = null
  modalError.value = ''
}

const saveBudget = async () => {
  saving.value = true
  modalError.value = ''
  
  try {
    if (editingBudget.value) {
      await $fetch(`/api/budgets/${editingBudget.value.id}`, {
        baseURL: config.public.apiUrl,
        method: 'PUT',
        headers: getAuthHeaders(),
        body: form
      })
      notifySuccess('Presupuesto actualizado', `${form.category}: $${formatNumber(form.amount)}`)
    } else {
      await $fetch('/api/budgets', {
        baseURL: config.public.apiUrl,
        method: 'POST',
        headers: getAuthHeaders(),
        body: form
      })
      notifySuccess('Presupuesto creado', `${form.category}: $${formatNumber(form.amount)}`)
    }
    closeModal()
    await fetchBudgets()
  } catch (e) {
    console.error('Error saving budget:', e)
    modalError.value = e?.data?.detail || 'Error al guardar el presupuesto'
    notifyError('Error', modalError.value)
  } finally {
    saving.value = false
  }
}

const confirmDelete = (budget) => {
  budgetToDelete.value = budget
  showDeleteModal.value = true
}

const deleteBudget = async () => {
  if (!budgetToDelete.value) return
  
  deleting.value = true
  try {
    await $fetch(`/api/budgets/${budgetToDelete.value.id}`, {
      baseURL: config.public.apiUrl,
      method: 'DELETE',
      headers: getAuthHeaders()
    })
    notifySuccess('Presupuesto eliminado', budgetToDelete.value.category)
    showDeleteModal.value = false
    budgetToDelete.value = null
    await fetchBudgets()
  } catch (e) {
    console.error('Error deleting budget:', e)
    notifyError('Error', 'No se pudo eliminar el presupuesto')
  } finally {
    deleting.value = false
  }
}

// Init
onMounted(() => {
  fetchBudgets()
})
</script>
