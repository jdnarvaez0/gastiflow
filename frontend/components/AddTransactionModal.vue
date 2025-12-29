<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Nuevo Movimiento</h3>
        <button class="close-btn" @click="close">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>
      
      <!-- Error Message -->
      <div v-if="errorMessage" class="error-message">
        <i class="fa-solid fa-exclamation-circle"></i>
        {{ errorMessage }}
      </div>

      <form @submit.prevent="saveTransaction">
        <div class="form-group">
          <label>Descripción</label>
          <input v-model="form.description" type="text" required placeholder="Ej: Compra semanal" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Monto</label>
            <input v-model.number="form.amount" type="number" step="0.01" required placeholder="0.00" />
          </div>
          
          <div class="form-group">
            <label>Tipo</label>
            <select v-model="form.transaction_type" required>
              <option value="expense">Gasto</option>
              <option value="income">Ingreso</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>Categoría</label>
          <select v-model="form.category" required>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>

        <div class="form-group">
          <label>Fecha</label>
          <input v-model="form.date" type="date" required />
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-secondary" @click="close">Cancelar</button>
          <button type="submit" class="btn-primary" :disabled="loading">
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

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--card-bg);
  padding: 2rem;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: var(--text-muted);
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  font-size: 0.9rem;
}

input, select {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  background-color: var(--bg-color);
  color: var(--text-color);
  font-family: inherit;
}

input:focus, select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-secondary {
  background-color: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-color);
  padding: 0.6rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.btn-secondary:hover {
  background-color: var(--bg-color);
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  color: #dc2626;
  font-size: 0.9rem;
}

.error-message i {
  flex-shrink: 0;
}

[data-theme="dark"] .error-message {
  background-color: rgba(220, 38, 38, 0.15);
  border-color: rgba(220, 38, 38, 0.3);
  color: #f87171;
}
</style>
