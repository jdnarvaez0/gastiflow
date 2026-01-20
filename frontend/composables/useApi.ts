export interface DashboardStats {
    income: number
    expenses: number
    balance: number
    savings: number
}

export interface CategoryStat {
    category: string
    amount: number
}

export interface HistoryStats {
    labels: string[]
    income: number[]
    expenses: number[]
}

export interface Expense {
    id: number
    description: string
    amount: number
    category: string
    date: string
    transaction_type: string
    currency: string
}

export interface DashboardData {
    stats: DashboardStats
    categories: CategoryStat[]
    history: HistoryStats
    expenses: Expense[]
    current_date: string
}

export const useApi = () => {
    const config = useRuntimeConfig()
    const apiUrl = config.public.apiUrl

    const getDashboardData = async () => {
        return await useFetch<DashboardData>('/api/dashboard', {
            baseURL: apiUrl,
            headers: {
                'ngrok-skip-browser-warning': 'true'
            }
        })
    }

    return {
        getDashboardData
    }
}
