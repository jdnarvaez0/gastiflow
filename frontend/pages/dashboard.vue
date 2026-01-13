<template>
  <div>
    <!-- Topbar -->
    <div class="flex justify-between items-center mb-6">
        <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ $t('dashboard.title') }}</div>
        <div class="flex items-center gap-4">
            <LanguageSwitcher />
            <button @click="toggleTheme" class="p-2 text-gray-500 dark:text-gray-400 hover:text-primary transition-colors">
                <i :class="isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon'" class="text-xl"></i>
            </button>
            <button @click="showAddModal = true" class="px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark transition-colors flex items-center gap-2">
                <i class="fa-solid fa-plus"></i> {{ $t('dashboard.newMovement') }}
            </button>
            <button class="p-2 text-gray-500 dark:text-gray-400 hover:text-primary transition-colors">
                <i class="fa-regular fa-bell text-xl"></i>
            </button>
            <UserAvatar 
                :image-url="user?.profile_picture_url" 
                :name="user?.full_name || user?.username"
                :username="user?.username"
                size="sm"
            />
        </div>
    </div>

    <AddTransactionModal :is-open="showAddModal" @close="showAddModal = false" @saved="refreshData" />

    <div v-if="pending" class="text-center py-8 text-gray-500 dark:text-gray-400">
        {{ $t('common.loading') }}
    </div>
    
    <div v-else-if="error" class="text-center py-8 text-red-500">
        Error cargando datos: {{ error.message }}
    </div>

    <div v-else>
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Balance Total -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <div class="flex justify-between items-start mb-4">
                    <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('dashboard.balance') }}</span>
                    <i class="fa-solid fa-wallet text-primary"></i>
                </div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white mb-2">${{ formatNumber(data?.stats?.balance) }}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">{{ $t('dashboard.updatedNow') }}</div>
            </div>

            <!-- Ingresos -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <div class="flex justify-between items-start mb-4">
                    <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('dashboard.incomeThisMonth') }}</span>
                    <i class="fa-solid fa-arrow-up text-success"></i>
                </div>
                <div class="text-2xl font-bold text-success mb-2">${{ formatNumber(data?.stats?.income) }}</div>
                <div class="text-xs text-success flex items-center gap-1">
                    <i class="fa-solid fa-arrow-trend-up"></i> +15.2% {{ $t('dashboard.vsLastMonth') }}
                </div>
            </div>

            <!-- Gastos -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <div class="flex justify-between items-start mb-4">
                    <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('dashboard.expensesThisMonth') }}</span>
                    <i class="fa-solid fa-arrow-down text-danger"></i>
                </div>
                <div class="text-2xl font-bold text-danger mb-2">${{ formatNumber(data?.stats?.expenses) }}</div>
                <div class="text-xs text-danger flex items-center gap-1">
                    <i class="fa-solid fa-arrow-trend-down"></i> +5.1% {{ $t('dashboard.vsLastMonth') }}
                </div>
            </div>

            <!-- Ahorro -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <div class="flex justify-between items-start mb-4">
                    <span class="text-sm text-gray-500 dark:text-gray-400">{{ $t('dashboard.savingsThisMonth') }}</span>
                    <i class="fa-solid fa-piggy-bank text-primary"></i>
                </div>
                <div class="text-2xl font-bold text-primary mb-2">${{ formatNumber(data?.stats?.savings) }}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">{{ $t('dashboard.objective') }}: $2,000,000.00</div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <!-- Main Chart -->
            <div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="font-semibold text-gray-900 dark:text-white">{{ $t('dashboard.expensesSummary') }}</h3>
                    <div class="flex gap-2">
                        <button class="px-3 py-1.5 bg-gray-100 dark:bg-gray-700 rounded-lg text-sm text-gray-700 dark:text-gray-300">{{ $t('dashboard.thisMonth') }}</button>
                        <button class="px-3 py-1.5 text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">{{ $t('dashboard.last6Months') }}</button>
                    </div>
                </div>
                <div class="relative h-72">
                    <canvas id="mainChart"></canvas>
                </div>
            </div>

            <!-- Categories -->
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
                <h3 class="font-semibold text-gray-900 dark:text-white mb-4">{{ $t('dashboard.categories') }}</h3>
                <div class="space-y-4">
                    <div v-for="cat in (data?.categories || []).slice(0, 5)" :key="cat.category" class="flex justify-between items-center">
                        <div class="flex items-center gap-3">
                            <div class="w-2 h-2 rounded-full bg-primary"></div>
                            <span class="text-gray-700 dark:text-gray-300">{{ $t('categories.' + cat.category) || cat.category }}</span>
                        </div>
                        <span class="font-semibold text-gray-900 dark:text-white">${{ formatNumber(cat.amount) }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Transactions -->
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-sm">
            <div class="flex justify-between items-center mb-6">
                <h3 class="font-semibold text-gray-900 dark:text-white">{{ $t('dashboard.recentMovements') }}</h3>
                <a href="#" class="text-primary text-sm hover:underline">{{ $t('dashboard.viewAll') }}</a>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead>
                        <tr class="border-b border-gray-200 dark:border-gray-700">
                            <th class="text-left py-3 text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('dashboard.description') }}</th>
                            <th class="text-left py-3 text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('dashboard.category') }}</th>
                            <th class="text-left py-3 text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('dashboard.date') }}</th>
                            <th class="text-right py-3 text-sm font-medium text-gray-500 dark:text-gray-400">{{ $t('dashboard.amount') }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="expense in (data?.expenses || [])" :key="expense.id" class="border-b border-gray-100 dark:border-gray-700 last:border-0">
                            <td class="py-4">
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 rounded-xl flex items-center justify-center"
                                        :class="expense.transaction_type == 'expense' ? 'bg-red-100 dark:bg-red-900/20 text-red-600' : 'bg-green-100 dark:bg-green-900/20 text-green-600'">
                                        <i :class="['fa-solid', getCategoryIcon(expense.category, expense.transaction_type)]"></i>
                                    </div>
                                    <div>
                                        <div class="font-medium text-gray-900 dark:text-white">{{ expense.description }}</div>
                                        <div class="text-xs text-gray-500 dark:text-gray-400">{{ expense.transaction_type }}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="py-4 text-gray-700 dark:text-gray-300">{{ expense.category }}</td>
                            <td class="py-4 text-gray-700 dark:text-gray-300">{{ formatDate(expense.date) }}</td>
                            <td class="py-4 text-right font-semibold" :class="expense.transaction_type == 'expense' ? 'text-danger' : 'text-success'">
                                {{ expense.transaction_type == 'expense' ? '-' : '+' }}${{ formatNumber(expense.amount) }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import AddTransactionModal from '~/components/AddTransactionModal.vue'

// Require authentication for this page
definePageMeta({
    middleware: 'auth'
})

const config = useRuntimeConfig()
const router = useRouter()
const { getAuthHeaders, isAuthenticated, token, init, user } = useAuth()

// Initialize auth on client side
const authReady = ref(false)
const data = ref(null)
const pending = ref(true)
const error = ref(null)

// Polling interval ref
const pollingInterval = ref(null)
const POLLING_INTERVAL_MS = 10000 // 10 seconds

// Fetch dashboard data
const fetchDashboard = async () => {
    if (!token.value) {
        data.value = { stats: { balance: 0, income: 0, expenses: 0, savings: 0 }, categories: [], history: { labels: [], income: [], expenses: [] }, expenses: [] }
        pending.value = false
        return
    }

    try {
        const response = await $fetch('/api/dashboard', {
            baseURL: config.public.apiUrl,
            headers: getAuthHeaders()
        })
        data.value = response
        error.value = null
    } catch (e) {
        error.value = e
        console.error('Error fetching dashboard:', e)
    } finally {
        pending.value = false
    }
}

// Refresh function for manual refresh and after adding transactions
const refresh = async () => {
    await fetchDashboard()
}

const showAddModal = ref(false)

const refreshData = async () => {
    await refresh()
}

const isDark = ref(false)

const toggleTheme = () => {
    isDark.value = !isDark.value
    if (isDark.value) {
        document.documentElement.setAttribute('data-theme', 'dark')
        document.documentElement.classList.add('dark')
        localStorage.setItem('theme', 'dark')
    } else {
        document.documentElement.removeAttribute('data-theme')
        document.documentElement.classList.remove('dark')
        localStorage.setItem('theme', 'light')
    }
}

// Start polling for updates
const startPolling = () => {
    if (pollingInterval.value) return
    pollingInterval.value = setInterval(async () => {
        if (token.value) {
            await fetchDashboard()
            if (data.value?.history) {
                renderChart(data.value.history)
            }
        }
    }, POLLING_INTERVAL_MS)
}

// Stop polling
const stopPolling = () => {
    if (pollingInterval.value) {
        clearInterval(pollingInterval.value)
        pollingInterval.value = null
    }
}

onMounted(async () => {
    await init()
    authReady.value = true
    await fetchDashboard()
    
    // Load saved theme - Default to dark theme for new users
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'light') {
        isDark.value = false
        document.documentElement.removeAttribute('data-theme')
        document.documentElement.classList.remove('dark')
    } else {
        isDark.value = true
        document.documentElement.setAttribute('data-theme', 'dark')
        document.documentElement.classList.add('dark')
    }

    if (data.value && data.value.history) {
        renderChart(data.value.history)
    }
    
    startPolling()
})

onUnmounted(() => {
    stopPolling()
})

const formatNumber = (num) => {
    return new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num || 0)
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString()
}

const getCategoryIcon = (category, type) => {
    if (type === 'income') return 'fa-money-bill-wave';
    
    const iconMap = {
        'Transporte': 'fa-bus',
        'Supermercado': 'fa-cart-shopping',
        'Restaurante': 'fa-utensils',
        'Comida': 'fa-burger',
        'Hogar': 'fa-house',
        'Servicios': 'fa-bolt',
        'Salud': 'fa-notes-medical',
        'Entretenimiento': 'fa-film',
        'Educación': 'fa-graduation-cap',
        'Ropa': 'fa-shirt',
        'Viajes': 'fa-plane',
        'Gasolina': 'fa-gas-pump',
        'Deportes': 'fa-dumbbell',
        'Mascotas': 'fa-paw',
        'Tecnología': 'fa-laptop',
        'Regalos': 'fa-gift'
    };

    return iconMap[category] || 'fa-bag-shopping';
}

watch(data, (newData) => {
    if (newData && newData.history) {
        renderChart(newData.history)
    }
})

const renderChart = (history) => {
    const ctx = document.getElementById('mainChart')
    if (!ctx) return

    const existingChart = Chart.getChart(ctx)
    if (existingChart) existingChart.destroy()

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: history.labels,
            datasets: [
                {
                    label: 'Ingresos',
                    data: history.income,
                    backgroundColor: '#4CE1B6',
                    borderRadius: 5,
                    barThickness: 20
                },
                {
                    label: 'Gastos',
                    data: history.expenses,
                    backgroundColor: '#FF754C',
                    borderRadius: 5,
                    barThickness: 20
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    align: 'end',
                    labels: {
                        usePointStyle: true,
                        boxWidth: 8
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        borderDash: [5, 5],
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    })
}
</script>
