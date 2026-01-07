<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black/50 flex justify-center items-center z-50" @click.self="close">
    <div class="bg-white dark:bg-gray-800 p-8 rounded-xl w-full max-w-md shadow-xl">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Nuevo Movimiento</h3>
        <button class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-xl" @click="close">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>
      
      <!-- Error Message -->
      <div v-if="errorMessage" class="flex items-center gap-2 px-4 py-3 mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm">
        <i class="fa-solid fa-exclamation-circle flex-shrink-0"></i>
        {{ errorMessage }}
      </div>

      <form @submit.prevent="saveTransaction">
        <div class="mb-4">
          <label class="block mb-2 font-medium text-sm text-gray-700 dark:text-gray-300">Descripción</label>
          <input 
            v-model="form.description" 
            type="text" 
            required 
            placeholder="Ej: Compra semanal"
            class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
          />
        </div>

        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block mb-2 font-medium text-sm text-gray-700 dark:text-gray-300">Monto</label>
            <input 
              v-model.number="form.amount" 
              type="number" 
              step="0.01" 
              required 
              placeholder="0.00"
              class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
            />
          </div>
          
          <div>
            <label class="block mb-2 font-medium text-sm text-gray-700 dark:text-gray-300">Tipo</label>
            <select 
              v-model="form.transaction_type" 
              required
              class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
            >
              <option value="expense">Gasto</option>
              <option value="income">Ingreso</option>
            </select>
          </div>
        </div>

        <div class="mb-4">
          <label class="block mb-2 font-medium text-sm text-gray-700 dark:text-gray-300">Categoría</label>
          <select 
            v-model="form.category" 
            required
            class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
          >
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>

        <div class="mb-6">
          <label class="block mb-2 font-medium text-sm text-gray-700 dark:text-gray-300">Fecha</label>
          <input 
            v-model="form.date" 
            type="date" 
            required
            class="w-full px-3 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
          />
        </div>

        <div class="flex justify-end gap-3">
          <button 
            type="button" 
            class="px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 font-medium hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            @click="close"
          >
            Cancelar
          </button>
          <button 
            type="submit" 
            class="px-4 py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            :disabled="loading"
          >
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'saved'])
const config = useRuntimeConfig()
const { getAuthHeaders, isAuthenticated } = useAuth()
const router = useRouter()

const loading = ref(false)
const errorMessage = ref('')
const form = reactive({
  description: '',
  amount: '',
  transaction_type: 'expense',
  category: 'Comida',
  date: new Date().toISOString().split('T')[0]
})

const categories = [
  'Comida', 'Transporte', 'Hogar', 'Servicios', 'Entretenimiento', 
  'Salud', 'Educación', 'Ropa', 'Viajes', 'Gasolina', 
  'Deportes', 'Mascotas', 'Tecnología', 'Regalos', 'Otros',
  'Salario', 'Freelance', 'Ventas', 'Inversiones'
]

const close = () => {
  errorMessage.value = ''
  emit('close')
  // Reset form slightly delayed to avoid visual glitch
  setTimeout(() => {
    form.description = ''
    form.amount = ''
    form.transaction_type = 'expense'
    form.category = 'Comida'
    form.date = new Date().toISOString().split('T')[0]
    errorMessage.value = ''
  }, 200)
}

const saveTransaction = async () => {
  errorMessage.value = ''
  
  // Check authentication before attempting to save
  if (!isAuthenticated.value) {
    errorMessage.value = 'Debes iniciar sesión para agregar movimientos.'
    return
  }
  
  loading.value = true
  try {
    await $fetch('/api/expenses', {
      baseURL: config.public.apiUrl,
      method: 'POST',
      headers: getAuthHeaders(),
      body: form
    })
    emit('saved')
    close()
  } catch (error) {
    console.error('Error saving transaction:', error)
    
    // Handle specific error codes
    const statusCode = error?.response?.status || error?.statusCode
    
    if (statusCode === 401) {
      errorMessage.value = 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
      setTimeout(() => {
        close()
        router.push('/login')
      }, 2000)
    } else if (statusCode === 400) {
      errorMessage.value = 'Datos inválidos. Por favor, revisa los campos e intenta de nuevo.'
    } else if (statusCode === 422) {
      errorMessage.value = 'Error de validación. Verifica que todos los campos estén correctos.'
    } else {
      errorMessage.value = 'Error al guardar el movimiento. Intenta de nuevo más tarde.'
    }
  } finally {
    loading.value = false
  }
}
</script>
