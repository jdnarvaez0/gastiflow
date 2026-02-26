<template>
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
        v-if="isOpen" 
        class="fixed inset-0 z-50 flex items-end sm:items-center justify-center"
        @click.self="close"
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
            v-if="isOpen"
            class="relative w-full sm:w-[480px] max-h-[90vh] sm:max-h-[85vh] bg-white dark:bg-gray-800 sm:rounded-2xl rounded-t-2xl shadow-2xl overflow-hidden flex flex-col"
          >
            <!-- Header -->
            <div class="flex-shrink-0 px-4 sm:px-6 py-4 bg-amber-500">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
                    <UIcon name="i-heroicons-pencil-square" class="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-white">Editar Movimiento</h3>
                  </div>
                </div>
                <button 
                  @click="close"
                  class="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"
                >
                  <UIcon name="i-heroicons-x-mark" class="w-5 h-5 text-white" />
                </button>
              </div>
            </div>
            
            <!-- Scrollable Content -->
            <div class="flex-1 overflow-y-auto overscroll-contain">
              <div class="p-4 sm:p-6 space-y-4">
                <!-- Type Toggle -->
                <div class="flex gap-1 p-1 bg-gray-100 dark:bg-gray-700 rounded-xl">
                  <button
                    type="button"
                    @click="form.transaction_type = 'expense'"
                    class="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-lg font-semibold text-sm transition-all"
                    :class="form.transaction_type === 'expense' 
                      ? 'bg-white dark:bg-gray-600 text-red-500 shadow-sm' 
                      : 'text-gray-500 dark:text-gray-400'"
                  >
                    <UIcon name="i-heroicons-arrow-trending-down" class="w-4 h-4" />
                    Gasto
                  </button>
                  <button
                    type="button"
                    @click="form.transaction_type = 'income'"
                    class="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-lg font-semibold text-sm transition-all"
                    :class="form.transaction_type === 'income' 
                      ? 'bg-white dark:bg-gray-600 text-emerald-500 shadow-sm' 
                      : 'text-gray-500 dark:text-gray-400'"
                  >
                    <UIcon name="i-heroicons-arrow-trending-up" class="w-4 h-4" />
                    Ingreso
                  </button>
                </div>
                
                <!-- Error Message -->
                <div 
                  v-if="errorMessage" 
                  class="flex items-start gap-2 px-4 py-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400 text-sm"
                >
                  <UIcon name="i-heroicons-exclamation-circle" class="w-5 h-5 flex-shrink-0" />
                  <span>{{ errorMessage }}</span>
                </div>
                
                <!-- Amount Field -->
                <div>
                  <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                    Monto
                  </label>
                  <div class="relative">
                    <span 
                      class="absolute left-4 top-1/2 -translate-y-1/2 text-xl font-bold"
                      :class="form.transaction_type === 'expense' ? 'text-red-500' : 'text-emerald-500'"
                    >
                      {{ form.transaction_type === 'expense' ? '-' : '+' }}$
                    </span>
                    <input 
                      v-model.number="form.amount" 
                      type="number" 
                      step="0.01" 
                      inputmode="decimal"
                      required 
                      placeholder="0.00"
                      class="w-full pl-12 pr-4 py-4 text-3xl font-bold bg-gray-50 dark:bg-gray-900 border-2 border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-white focus:outline-none transition-colors placeholder:text-gray-300"
                      :class="form.transaction_type === 'expense' ? 'focus:border-red-500' : 'focus:border-emerald-500'"
                    />
                  </div>
                </div>
                
                <!-- Description Field -->
                <div>
                  <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                    Descripción
                  </label>
                  <input 
                    v-model="form.description" 
                    type="text" 
                    required 
                    placeholder="Ej: Compra semanal"
                    class="w-full px-4 py-3.5 bg-gray-50 dark:bg-gray-900 border-2 border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-white focus:outline-none transition-colors"
                    :class="form.transaction_type === 'expense' ? 'focus:border-red-500' : 'focus:border-emerald-500'"
                  />
                </div>
                
                <!-- Category -->
                <div>
                  <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                    Categoría
                  </label>
                  <div class="grid grid-cols-3 gap-2">
                    <button
                      v-for="cat in filteredCategories"
                      :key="cat.value"
                      type="button"
                      @click="form.category = cat.value"
                      class="flex flex-col items-center gap-1.5 p-3 rounded-xl border-2 transition-all min-h-[72px] justify-center"
                      :class="form.category === cat.value 
                        ? form.transaction_type === 'expense'
                          ? 'border-red-500 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400'
                          : 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400'
                        : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400'
                      "
                    >
                      <UIcon :name="cat.icon" class="w-5 h-5" />
                      <span class="text-xs font-medium leading-tight">{{ cat.label }}</span>
                    </button>
                  </div>
                </div>
                
                <!-- Date Field -->
                <div>
                  <label class="block mb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">
                    Fecha
                  </label>
                  <input 
                    v-model="form.date" 
                    type="date" 
                    required
                    class="w-full px-4 py-3.5 bg-gray-50 dark:bg-gray-900 border-2 border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-white focus:outline-none transition-colors"
                    :class="form.transaction_type === 'expense' ? 'focus:border-red-500' : 'focus:border-emerald-500'"
                  />
                </div>
              </div>
            </div>
            
            <!-- Footer Buttons (Sticky) -->
            <div class="flex-shrink-0 p-4 sm:p-6 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
              <div class="flex gap-3">
                <button 
                  type="button" 
                  @click="close"
                  class="flex-1 px-4 py-3.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-xl active:scale-95 transition-transform"
                >
                  Cancelar
                </button>
                <button 
                  type="button"
                  @click="saveTransaction"
                  class="flex-1 px-4 py-3.5 bg-amber-500 text-white font-semibold rounded-xl active:scale-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                  :disabled="loading || !isFormValid"
                >
                  <UIcon v-if="loading" name="i-heroicons-arrow-path" class="w-5 h-5 animate-spin" />
                  <span v-else>Guardar</span>
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  isOpen: Boolean,
  transaction: Object
})

const emit = defineEmits(['close', 'saved'])
const config = useRuntimeConfig()
const { getAuthHeaders, isAuthenticated } = useAuth()
const router = useRouter()
const { success: notifySuccess, error: notifyError } = useNotification()

const loading = ref(false)
const errorMessage = ref('')

const allCategories = [
  { value: 'Comida', label: 'Comida', icon: 'i-heroicons-cake', type: 'expense' },
  { value: 'Transporte', label: 'Transporte', icon: 'i-heroicons-truck', type: 'expense' },
  { value: 'Hogar', label: 'Hogar', icon: 'i-heroicons-home', type: 'expense' },
  { value: 'Servicios', label: 'Servicios', icon: 'i-heroicons-bolt', type: 'expense' },
  { value: 'Entretenimiento', label: 'Entretenimiento', icon: 'i-heroicons-ticket', type: 'expense' },
  { value: 'Salud', label: 'Salud', icon: 'i-heroicons-heart', type: 'expense' },
  { value: 'Educación', label: 'Educación', icon: 'i-heroicons-academic-cap', type: 'expense' },
  { value: 'Ropa', label: 'Ropa', icon: 'i-heroicons-shopping-bag', type: 'expense' },
  { value: 'Viajes', label: 'Viajes', icon: 'i-heroicons-paper-airplane', type: 'expense' },
  { value: 'Gasolina', label: 'Gasolina', icon: 'i-heroicons-fire', type: 'expense' },
  { value: 'Deportes', label: 'Deportes', icon: 'i-heroicons-trophy', type: 'expense' },
  { value: 'Mascotas', label: 'Mascotas', icon: 'i-heroicons-face-smile', type: 'expense' },
  { value: 'Tecnología', label: 'Tecnología', icon: 'i-heroicons-computer-desktop', type: 'expense' },
  { value: 'Regalos', label: 'Regalos', icon: 'i-heroicons-gift', type: 'expense' },
  { value: 'Otros', label: 'Otros', icon: 'i-heroicons-tag', type: 'expense' },
  { value: 'Salario', label: 'Salario', icon: 'i-heroicons-banknotes', type: 'income' },
  { value: 'Freelance', label: 'Freelance', icon: 'i-heroicons-briefcase', type: 'income' },
  { value: 'Ventas', label: 'Ventas', icon: 'i-heroicons-currency-dollar', type: 'income' },
  { value: 'Inversiones', label: 'Inversiones', icon: 'i-heroicons-chart-bar', type: 'income' },
]

const filteredCategories = computed(() => {
  return allCategories.filter(cat => cat.type === form.transaction_type)
})

const form = reactive({
  description: '',
  amount: '',
  transaction_type: 'expense',
  category: 'Comida',
  date: ''
})

watch(() => props.transaction, (newTransaction) => {
  if (newTransaction) {
    form.description = newTransaction.description || ''
    form.amount = newTransaction.amount || ''
    form.transaction_type = newTransaction.transaction_type || 'expense'
    form.category = newTransaction.category || 'Comida'
    if (newTransaction.date) {
      const d = new Date(newTransaction.date)
      const offset = d.getTimezoneOffset()
      const localDate = new Date(d.getTime() + offset * 60000)
      form.date = localDate.toISOString().split('T')[0]
    } else {
      form.date = new Date().toISOString().split('T')[0]
    }
  }
}, { immediate: true })

watch(() => form.transaction_type, () => {
  const valid = filteredCategories.value
  if (!valid.find(c => c.value === form.category)) {
    form.category = valid[0]?.value || 'Comida'
  }
})

const isFormValid = computed(() => {
  return form.description.trim() && form.amount && form.amount > 0 && form.category && form.date
})

const close = () => {
  errorMessage.value = ''
  emit('close')
}

const saveTransaction = async () => {
  errorMessage.value = ''
  
  if (!isAuthenticated.value) {
    errorMessage.value = 'Debes iniciar sesión para editar movimientos.'
    return
  }
  
  if (!props.transaction?.id) {
    errorMessage.value = 'Error: No se encontró el movimiento.'
    return
  }
  
  loading.value = true
  try {
    await $fetch(`/api/expenses/${props.transaction.id}`, {
      baseURL: config.public.apiUrl,
      method: 'PUT',
      headers: getAuthHeaders(),
      body: form
    })
    
    notifySuccess('Movimiento actualizado', `${form.description} - $${form.amount}`)
    emit('saved')
    close()
  } catch (error) {
    console.error('Error updating transaction:', error)
    const statusCode = error?.response?.status || error?.statusCode
    
    if (statusCode === 401) {
      errorMessage.value = 'Tu sesión ha expirado.'
      setTimeout(() => { close(); router.push('/login') }, 2000)
    } else if (statusCode === 403) {
      errorMessage.value = 'No tienes permiso para editar este movimiento.'
    } else if (statusCode === 404) {
      errorMessage.value = 'Movimiento no encontrado.'
    } else {
      errorMessage.value = 'Error al actualizar. Intenta de nuevo.'
    }
    
    notifyError('Error', errorMessage.value)
  } finally {
    loading.value = false
  }
}
</script>
