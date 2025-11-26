<template>
  <div>
    <!-- Topbar -->
    <div class="topbar">
        <div class="page-title">Dashboard</div>
        <div class="user-actions">
            <div class="theme-switcher" style="display: flex; gap: 10px; align-items: center; margin-right: 15px;">
                <button @click="toggleTheme" style="background: none; border: none; cursor: pointer; color: var(--text-color); font-size: 1.2rem;">
                    <i :class="isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i>
                </button>
            </div>
            <a href="#" class="btn-primary">
                <i class="fa-solid fa-plus"></i> Nuevo Movimiento
            </a>
            <div class="notifications">
                <i class="fa-regular fa-bell"
                    style="font-size: 1.2rem; color: var(--secondary-color); cursor: pointer;"></i>
            </div>
            <div class="user-profile">
                <div style="width: 40px; height: 40px; background-color: #E2E8F0; border-radius: 50%;">
                    <img src="https://avatars.githubusercontent.com/u/739984?v=4" alt="Avatar" style="width: 100%; height: 100%; border-radius: 50%;">
                </div>
            </div>
        </div>
    </div>

    <div v-if="pending" style="text-align: center; padding: 2rem;">
        Cargando datos...
    </div>
    
    <div v-else-if="error" style="color: var(--danger-color); text-align: center;">
        Error cargando datos: {{ error.message }}
    </div>

    <div v-else>
        <!-- Summary Cards -->
        <div class="dashboard-grid">
            <!-- Balance Total -->
            <div class="stat-card">
                <div class="stat-header">
                    <span>Balance Total</span>
                    <i class="fa-solid fa-wallet"></i>
                </div>
                <div class="stat-value">${{ formatNumber(data?.stats?.balance) }}</div>
                <div class="stat-trend">Actualizado ahora mismo</div>
            </div>

            <!-- Ingresos -->
            <div class="stat-card">
                <div class="stat-header">
                    <span>Ingresos (este mes)</span>
                    <i class="fa-solid fa-arrow-up text-success"></i>
                </div>
                <div class="stat-value text-success">${{ formatNumber(data?.stats?.income) }}</div>
                <div class="stat-trend trend-up">
                    <i class="fa-solid fa-arrow-trend-up"></i> +15.2% vs mes anterior
                </div>
            </div>

            <!-- Gastos -->
            <div class="stat-card">
                <div class="stat-header">
                    <span>Gastos (este mes)</span>
                    <i class="fa-solid fa-arrow-down text-danger"></i>
                </div>
                <div class="stat-value text-danger">${{ formatNumber(data?.stats?.expenses) }}</div>
                <div class="stat-trend trend-down">
                    <i class="fa-solid fa-arrow-trend-down"></i> +5.1% vs mes anterior
                </div>
            </div>

            <!-- Ahorro -->
            <div class="stat-card">
                <div class="stat-header">
                    <span>Ahorro (este mes)</span>
                    <i class="fa-solid fa-piggy-bank"></i>
                </div>
                <div class="stat-value text-primary">${{ formatNumber(data?.stats?.savings) }}</div>
                <div class="stat-trend">Objetivo: $2,000,000.00</div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="charts-section">
            <!-- Main Chart -->
            <div class="chart-card">
                <div class="chart-header">
                    <h3>Resumen de Gastos</h3>
                    <div class="chart-actions">
                        <button
                            style="border: none; background: #F3F4F6; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Este
                            Mes</button>
                        <button
                            style="border: none; background: transparent; padding: 5px 10px; color: var(--secondary-color); cursor: pointer;">Últimos
                            6 meses</button>
                    </div>
                </div>
                <div style="position: relative; height: 300px; width: 100%;">
                    <canvas id="mainChart"></canvas>
                </div>
            </div>

            <!-- Categories -->
            <div class="chart-card">
                <div class="chart-header">
                    <h3>Categorías</h3>
                </div>
                <div class="category-list">
                    <div v-for="cat in (data?.categories || []).slice(0, 5)" :key="cat.category" class="category-item">
                        <div class="cat-info">
                            <div class="cat-dot" style="background-color: var(--primary-color);"></div>
                            <span>{{ cat.category }}</span>
                        </div>
                        <span style="font-weight: 600;">${{ formatNumber(cat.amount) }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Transactions -->
        <div class="recent-transactions">
            <div class="chart-header">
                <h3>Movimientos Recientes</h3>
                <a href="#" style="color: var(--primary-color); text-decoration: none; font-size: 0.9rem;">Ver Todos</a>
            </div>
            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>Descripción</th>
                            <th>Categoría</th>
                            <th>Fecha</th>
                            <th style="text-align: right;">Monto</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="expense in (data?.expenses || [])" :key="expense.id">
                            <td>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div class="icon-circle"
                                        :style="{ backgroundColor: expense.transaction_type == 'expense' ? '#EAD4FF' : '#D4FFE4', color: expense.transaction_type == 'expense' ? '#6C5DD3' : '#4CE1B6' }">
                                        <i :class="['fa-solid', getCategoryIcon(expense.category, expense.transaction_type)]"></i>
                                    </div>
                                    <div>
                                        <div style="font-weight: 600;">{{ expense.description }}</div>
                                        <div style="font-size: 0.8rem; color: var(--secondary-color);">{{ expense.transaction_type }}</div>
                                    </div>
                                </div>
                            </td>
                            <td>{{ expense.category }}</td>
                            <td>{{ formatDate(expense.date) }}</td>
                            <td style="text-align: right; font-weight: 600;"
                                :class="expense.transaction_type == 'expense' ? 'amount-negative' : 'amount-positive'">
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
const config = useRuntimeConfig()
const { data, pending, error } = await useFetch('/api/dashboard', {
    baseURL: config.public.apiUrl
})

const isDark = ref(false)

const toggleTheme = () => {
    isDark.value = !isDark.value
    if (isDark.value) {
        document.documentElement.setAttribute('data-theme', 'dark')
        localStorage.setItem('theme', 'dark')
    } else {
        document.documentElement.removeAttribute('data-theme')
        localStorage.setItem('theme', 'light')
    }
}

onMounted(() => {
    // Load saved theme
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'dark') {
        isDark.value = true
        document.documentElement.setAttribute('data-theme', 'dark')
    }

    if (data.value && data.value.history) {
        renderChart(data.value.history)
    }
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

onMounted(() => {
    if (data.value && data.value.history) {
        renderChart(data.value.history)
    }
})

watch(data, (newData) => {
    if (newData && newData.history) {
        renderChart(newData.history)
    }
})

const renderChart = (history) => {
    const ctx = document.getElementById('mainChart')
    if (!ctx) return

    // Destroy existing chart if any (basic check)
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
