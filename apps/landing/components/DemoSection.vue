<template>
  <section class="px-6 lg:px-24 py-24 bg-black/20">
    <div class="text-center mb-16">
      <div class="inline-flex items-center gap-2 px-4 py-2 bg-primary/15 border border-primary/30 rounded-full text-sm text-primary mb-6">
        <UIcon name="i-heroicons-eye" class="w-4 h-4" />
        <span>Demo interactiva</span>
      </div>
      <h2 class="text-3xl lg:text-4xl font-bold mb-4 font-display">
        Así de <span class="bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">fácil</span> es usar Gastiflow
      </h2>
      <p class="text-lg text-gray-400 max-w-2xl mx-auto">
        Registra gastos en segundos desde Telegram y visualiza todo en tu dashboard
      </p>
    </div>

    <!-- Demo Container -->
    <div class="max-w-6xl mx-auto">
      <!-- Tabs -->
      <div class="flex justify-center gap-2 mb-8 flex-wrap">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-4 py-2 rounded-xl font-medium transition-all"
          :class="activeTab === tab.id 
            ? 'bg-primary text-white' 
            : 'bg-gray-800 text-gray-400 hover:bg-gray-700'"
        >
          <UIcon :name="tab.icon" class="w-4 h-4 inline mr-2" />
          {{ tab.label }}
        </button>
      </div>

      <!-- Demo Content -->
      <div class="relative">
        <!-- Dashboard Demo -->
        <Transition
          enter-active-class="transition duration-500 ease-out"
          enter-from-class="opacity-0 translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-300 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-4"
        >
          <div v-if="activeTab === 'dashboard'" class="space-y-6">
            <!-- Mock Dashboard -->
            <div class="bg-gray-900 rounded-2xl border border-gray-700 overflow-hidden shadow-2xl">
              <!-- Mock Header -->
              <div class="bg-gray-800 px-6 py-4 border-b border-gray-700 flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                    <UIcon name="i-heroicons-wallet" class="w-4 h-4 text-primary" />
                  </div>
                  <span class="font-semibold">Gastiflow</span>
                </div>
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-accent to-accent-light"></div>
                </div>
              </div>

              <!-- Mock Content -->
              <div class="p-6 space-y-6">
                <!-- Stats Cards -->
                <div class="grid grid-cols-3 gap-4">
                  <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <p class="text-xs text-gray-400 mb-1">Balance</p>
                    <p class="text-xl font-bold text-white">$2.450.000</p>
                  </div>
                  <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <p class="text-xs text-gray-400 mb-1">Ingresos</p>
                    <p class="text-xl font-bold text-emerald-400">+$3.200.000</p>
                  </div>
                  <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
                    <p class="text-xs text-gray-400 mb-1">Gastos</p>
                    <p class="text-xl font-bold text-red-400">-$750.000</p>
                  </div>
                </div>

                <!-- Chart Placeholder -->
                <div class="bg-gray-800 rounded-xl p-4 border border-gray-700 h-40 flex items-end justify-around">
                  <div v-for="(h, i) in [40, 65, 45, 80, 55, 70, 60]" :key="i" 
                    class="w-8 bg-gradient-to-t from-primary to-accent rounded-t-lg opacity-80"
                    :style="{ height: h + '%' }"
                  />
                </div>

                <!-- Recent Transactions -->
                <div class="space-y-2">
                  <div v-for="(t, i) in mockTransactions" :key="i" 
                    class="flex items-center gap-3 p-3 bg-gray-800 rounded-xl border border-gray-700"
                  >
                    <div :class="`w-10 h-10 rounded-xl flex items-center justify-center ${t.color}`">
                      <UIcon :name="t.icon" class="w-5 h-5" />
                    </div>
                    <div class="flex-1">
                      <p class="font-medium text-sm">{{ t.name }}</p>
                      <p class="text-xs text-gray-400">{{ t.category }}</p>
                    </div>
                    <p :class="`font-bold ${t.amount > 0 ? 'text-emerald-400' : 'text-red-400'}`">
                      {{ t.amount > 0 ? '+' : '' }}${{ formatNumber(Math.abs(t.amount)) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Feature Highlights -->
            <div class="grid sm:grid-cols-3 gap-4">
              <div class="flex items-center gap-3 p-4 bg-gray-800/50 rounded-xl border border-gray-700">
                <UIcon name="i-heroicons-chart-pie" class="w-8 h-8 text-accent" />
                <div>
                  <p class="font-semibold text-sm">Análisis detallado</p>
                  <p class="text-xs text-gray-400">Por categoría y mes</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-4 bg-gray-800/50 rounded-xl border border-gray-700">
                <UIcon name="i-heroicons-wallet" class="w-8 h-8 text-primary" />
                <div>
                  <p class="font-semibold text-sm">Presupuestos</p>
                  <p class="text-xs text-gray-400">Alertas inteligentes</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-4 bg-gray-800/50 rounded-xl border border-gray-700">
                <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 text-emerald-400" />
                <div>
                  <p class="font-semibold text-sm">Tiempo real</p>
                  <p class="text-xs text-gray-400">Sincronización instantánea</p>
                </div>
              </div>
            </div>
          </div>
        </Transition>

        <!-- Telegram Bot Demo -->
        <Transition
          enter-active-class="transition duration-500 ease-out"
          enter-from-class="opacity-0 translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-300 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-4"
        >
          <div v-if="activeTab === 'telegram'" class="max-w-md mx-auto">
            <!-- Phone Frame -->
            <div class="bg-gray-900 rounded-[2.5rem] p-4 border-4 border-gray-800 shadow-2xl">
              <!-- Screen -->
              <div class="bg-[#0e1621] rounded-[2rem] overflow-hidden min-h-[500px] flex flex-col">
                <!-- Telegram Header -->
                <div class="bg-[#17212b] px-4 py-3 flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#0088cc] to-[#00a8e8] flex items-center justify-center">
                    <UIcon name="i-heroicons-wallet" class="w-5 h-5 text-white" />
                  </div>
                  <div class="flex-1">
                    <p class="font-semibold text-sm">Gastiflow Bot</p>
                    <p class="text-xs text-[#5eb5f7]">bot</p>
                  </div>
                </div>

                <!-- Chat Messages -->
                <div class="flex-1 p-4 space-y-4 overflow-y-auto">
                  <!-- Bot Message -->
                  <div class="flex gap-2">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#0088cc] to-[#00a8e8] flex-shrink-0 flex items-center justify-center">
                      <UIcon name="i-heroicons-wallet" class="w-4 h-4 text-white" />
                    </div>
                    <div class="bg-[#182533] rounded-2xl rounded-tl-none px-4 py-2 max-w-[80%]">
                      <p class="text-sm">¡Hola! 👋 Soy tu asistente financiero. Envíame un mensaje con tu gasto, una foto de un ticket, o usa estos comandos:</p>
                      <div class="mt-2 space-y-1">
                        <p class="text-xs text-[#5eb5f7]">/gasto $50.000 almuerzo</p>
                        <p class="text-xs text-[#5eb5f7]">/ingreso $1.000.000 salario</p>
                        <p class="text-xs text-[#5eb5f7]">/resumen</p>
                      </div>
                    </div>
                  </div>

                  <!-- User Messages with animation -->
                  <TransitionGroup enter-active-class="transition duration-500" enter-from-class="opacity-0 translate-x-4">
                    <div v-for="(msg, idx) in visibleMessages" :key="idx" 
                      class="flex gap-2 justify-end"
                    >
                      <div class="bg-[#2b5278] rounded-2xl rounded-tr-none px-4 py-2 max-w-[80%]">
                        <p class="text-sm">{{ msg.text }}</p>
                        <p class="text-[10px] text-right mt-1 opacity-60">
                          {{ msg.time }} <span v-if="msg.read">✓✓</span>
                        </p>
                      </div>
                    </div>
                  </TransitionGroup>

                  <!-- Typing indicator -->
                  <div v-if="isTyping" class="flex gap-2">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#0088cc] to-[#00a8e8] flex-shrink-0 flex items-center justify-center">
                      <UIcon name="i-heroicons-wallet" class="w-4 h-4 text-white" />
                    </div>
                    <div class="bg-[#182533] rounded-2xl rounded-tl-none px-4 py-3 flex items-center gap-1">
                      <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"></span>
                      <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
                      <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
                    </div>
                  </div>
                </div>

                <!-- Input Area -->
                <div class="bg-[#17212b] px-4 py-3 flex items-center gap-2">
                  <div class="w-10 h-10 rounded-full bg-gray-700/50 flex items-center justify-center">
                    <UIcon name="i-heroicons-paper-clip" class="w-5 h-5 text-gray-400" />
                  </div>
                  <div class="flex-1 bg-[#242f3d] rounded-full px-4 py-2 text-sm text-gray-400">
                    Mensaje
                  </div>
                  <div class="w-10 h-10 rounded-full bg-[#2b5278] flex items-center justify-center">
                    <UIcon name="i-heroicons-microphone" class="w-5 h-5 text-white" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Controls -->
            <div class="flex justify-center gap-4 mt-6">
              <button 
                @click="restartTelegramDemo"
                class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-xl text-sm font-medium transition-colors flex items-center gap-2"
              >
                <UIcon name="i-heroicons-arrow-path" class="w-4 h-4" />
                Ver de nuevo
              </button>
            </div>
          </div>
        </Transition>

        <!-- Presupuestos Demo -->
        <Transition
          enter-active-class="transition duration-500 ease-out"
          enter-from-class="opacity-0 translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-300 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-4"
        >
          <div v-if="activeTab === 'budgets'" class="space-y-6">
            <div class="bg-gray-900 rounded-2xl border border-gray-700 overflow-hidden shadow-2xl p-6">
              <h3 class="text-lg font-semibold mb-6">Tus Presupuestos</h3>
              
              <div class="space-y-4">
                <div v-for="(budget, i) in mockBudgets" :key="i" 
                  class="p-4 bg-gray-800 rounded-xl border border-gray-700"
                >
                  <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center gap-3">
                      <div :class="`w-10 h-10 rounded-xl flex items-center justify-center ${budget.color}`">
                        <UIcon :name="budget.icon" class="w-5 h-5" />
                      </div>
                      <div>
                        <p class="font-semibold">{{ budget.name }}</p>
                        <p class="text-xs text-gray-400">Límite: ${{ formatNumber(budget.limit) }}</p>
                      </div>
                    </div>
                    <span :class="`text-sm font-bold ${budget.percentage > 90 ? 'text-red-400' : 'text-emerald-400'}`">
                      {{ budget.percentage }}%
                    </span>
                  </div>
                  
                  <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div 
                      class="h-full rounded-full transition-all duration-1000"
                      :class="budget.percentage > 90 ? 'bg-red-500' : budget.percentage > 75 ? 'bg-amber-500' : 'bg-emerald-500'"
                      :style="{ width: budget.percentage + '%' }"
                    />
                  </div>
                  
                  <div class="flex justify-between mt-2 text-xs">
                    <span class="text-gray-400">${{ formatNumber(budget.spent) }} gastado</span>
                    <span v-if="budget.percentage > 90" class="text-red-400 flex items-center gap-1">
                      <UIcon name="i-heroicons-exclamation-circle" class="w-3 h-3" />
                      ¡Alerta!
                    </span>
                    <span v-else class="text-emerald-400">${{ formatNumber(budget.remaining) }} restante</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Alert Example -->
            <div class="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/30 rounded-xl">
              <UIcon name="i-heroicons-exclamation-triangle" class="w-6 h-6 text-red-400 flex-shrink-0" />
              <div class="flex-1">
                <p class="font-medium text-red-400 text-sm">Alerta de presupuesto</p>
                <p class="text-xs text-red-400/70">Has usado el 95% de tu presupuesto en Entretenimiento</p>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- CTA -->
    <div class="text-center mt-12">
      <p class="text-gray-400 mb-4">¿Listo para probarlo?</p>
      <a
        href="http://localhost:3000/register"
        class="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-accent to-accent-light text-white rounded-xl font-semibold hover:-translate-y-1 hover:shadow-lg hover:shadow-accent/40 transition-all text-lg"
      >
        <UIcon name="i-heroicons-rocket-launch" class="w-5 h-5" />
        Crear cuenta gratis
      </a>
    </div>
  </section>
</template>

<script setup>
const activeTab = ref('dashboard')
const isTyping = ref(false)
const visibleMessages = ref([])

const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: 'i-heroicons-chart-pie' },
  { id: 'telegram', label: 'Bot Telegram', icon: 'i-heroicons-chat-bubble-left-right' },
  { id: 'budgets', label: 'Presupuestos', icon: 'i-heroicons-wallet' },
]

const mockTransactions = [
  { name: 'Supermercado Éxito', category: 'Comida', amount: -125000, icon: 'i-heroicons-shopping-cart', color: 'bg-orange-500/20 text-orange-400' },
  { name: 'Uber', category: 'Transporte', amount: -28000, icon: 'i-heroicons-truck', color: 'bg-blue-500/20 text-blue-400' },
  { name: 'Salario Mensual', category: 'Ingresos', amount: 3200000, icon: 'i-heroicons-banknotes', color: 'bg-emerald-500/20 text-emerald-400' },
  { name: 'Netflix', category: 'Entretenimiento', amount: -45000, icon: 'i-heroicons-ticket', color: 'bg-purple-500/20 text-purple-400' },
]

const mockBudgets = [
  { name: 'Comida', limit: 600000, spent: 450000, remaining: 150000, percentage: 75, icon: 'i-heroicons-cake', color: 'bg-orange-500/20 text-orange-400' },
  { name: 'Transporte', limit: 300000, spent: 95000, remaining: 205000, percentage: 32, icon: 'i-heroicons-truck', color: 'bg-blue-500/20 text-blue-400' },
  { name: 'Entretenimiento', limit: 200000, spent: 190000, remaining: 10000, percentage: 95, icon: 'i-heroicons-ticket', color: 'bg-red-500/20 text-red-400' },
]

const telegramMessages = [
  { text: 'Gasté $45.000 en almuerzo de trabajo', time: '14:30', read: true },
  { text: '/resumen', time: '14:32', read: true },
]

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO').format(num)
}

const restartTelegramDemo = () => {
  visibleMessages.value = []
  startTelegramDemo()
}

const startTelegramDemo = async () => {
  await new Promise(r => setTimeout(r, 1000))
  
  for (const msg of telegramMessages) {
    isTyping.value = true
    await new Promise(r => setTimeout(r, 1500))
    isTyping.value = false
    visibleMessages.value.push(msg)
    await new Promise(r => setTimeout(r, 800))
  }
}

onMounted(() => {
  startTelegramDemo()
})

watch(activeTab, (newTab) => {
  if (newTab === 'telegram') {
    visibleMessages.value = []
    startTelegramDemo()
  }
})
</script>
