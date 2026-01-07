<template>
    <div class="text-white">
        <!-- Hero Section -->
        <section class="min-h-[calc(100vh-80px)] grid lg:grid-cols-2 gap-16 items-center px-6 lg:px-24 py-16 relative overflow-hidden">
            <!-- Gradient background -->
            <div class="absolute -top-1/2 -right-1/5 w-4/5 h-[150%] bg-[radial-gradient(circle,rgba(147,51,234,0.15)_0%,transparent_70%)] pointer-events-none"></div>
            
            <div class="relative z-10 lg:text-left text-center">
                <div class="inline-flex items-center gap-2 px-4 py-2 bg-accent/15 border border-accent/30 rounded-full text-sm text-accent mb-6">
                    <i class="fas fa-bolt"></i>
                    <span>Gestión financiera inteligente</span>
                </div>
                <h1 class="text-4xl lg:text-6xl font-bold leading-tight mb-6 font-display">
                    Toma el control de tus
                    <span class="bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">finanzas personales</span>
                </h1>
                <p class="text-lg lg:text-xl text-gray-400 leading-relaxed mb-8 max-w-xl lg:mx-0 mx-auto">
                    Registra gastos con facilidad, analiza tus hábitos financieros y alcanza tus metas de ahorro. 
                    Todo en un solo lugar, con la ayuda de inteligencia artificial.
                </p>
                <div class="flex gap-4 mb-12 flex-wrap lg:justify-start justify-center">
                    <NuxtLink to="/register" class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-accent to-accent-light text-white rounded-xl font-semibold hover:-translate-y-1 hover:shadow-lg hover:shadow-accent/40 transition-all">
                        <i class="fas fa-rocket"></i>
                        Comenzar Gratis
                    </NuxtLink>
                    <NuxtLink to="/login" class="inline-flex items-center gap-2 px-8 py-4 border border-gray-600 text-white rounded-xl font-semibold hover:bg-white/5 hover:border-accent transition-all">
                        <i class="fas fa-sign-in-alt"></i>
                        Ya tengo cuenta
                    </NuxtLink>
                </div>
                <div class="flex items-center gap-8 lg:justify-start justify-center">
                    <div class="text-center">
                        <span class="block text-2xl font-bold">100%</span>
                        <span class="text-sm text-gray-400">Gratis</span>
                    </div>
                    <div class="w-px h-10 bg-gray-600"></div>
                    <div class="text-center">
                        <span class="block text-2xl font-bold text-accent"><i class="fab fa-telegram"></i></span>
                        <span class="text-sm text-gray-400">Integración</span>
                    </div>
                    <div class="w-px h-10 bg-gray-600"></div>
                    <div class="text-center">
                        <span class="block text-2xl font-bold text-accent"><i class="fas fa-brain"></i></span>
                        <span class="text-sm text-gray-400">Con IA</span>
                    </div>
                </div>
            </div>
            <div class="relative h-[500px] hidden lg:block">
                <div class="absolute top-[10%] right-[20%] bg-landing-card border border-gray-700 rounded-2xl p-6 shadow-2xl animate-float">
                    <i class="fas fa-arrow-up text-success text-2xl mb-2"></i>
                    <span class="block font-semibold text-lg">+$250,000</span>
                    <small class="text-gray-400">Ingreso registrado</small>
                </div>
                <div class="absolute top-[40%] right-[5%] bg-landing-card border border-gray-700 rounded-2xl p-6 shadow-2xl animate-float animation-delay-2000">
                    <i class="fas fa-chart-pie text-2xl text-accent mb-2"></i>
                    <span class="block font-semibold text-lg">Análisis</span>
                    <small class="text-gray-400">En tiempo real</small>
                </div>
                <div class="absolute bottom-[15%] right-[25%] bg-landing-card border border-gray-700 rounded-2xl p-6 shadow-2xl animate-float animation-delay-4000">
                    <i class="fas fa-piggy-bank text-primary text-2xl mb-2"></i>
                    <span class="block font-semibold text-lg">Meta: 80%</span>
                    <small class="text-gray-400">Ahorro mensual</small>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="px-6 lg:px-24 py-24 bg-black/20">
            <div class="text-center mb-16">
                <h2 class="text-3xl lg:text-4xl font-bold mb-4 font-display">Todo lo que necesitas para gestionar tu dinero</h2>
                <p class="text-lg text-gray-400">Herramientas poderosas diseñadas para simplificar tu vida financiera</p>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
                <div class="bg-landing-card border border-gray-700 rounded-2xl p-8 text-center hover:-translate-y-2 hover:border-accent hover:shadow-xl hover:shadow-accent/15 transition-all">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-accent/20 rounded-2xl text-3xl text-accent">
                        <i class="fas fa-mobile-alt"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Registro Fácil</h3>
                    <p class="text-gray-400 leading-relaxed">Registra tus gastos e ingresos en segundos desde cualquier dispositivo.</p>
                </div>
                <div class="bg-landing-card border border-gray-700 rounded-2xl p-8 text-center hover:-translate-y-2 hover:border-accent hover:shadow-xl hover:shadow-accent/15 transition-all">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-[#0088cc]/20 rounded-2xl text-3xl text-[#0088cc]">
                        <i class="fab fa-telegram"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Bot de Telegram</h3>
                    <p class="text-gray-400 leading-relaxed">Registra gastos desde Telegram con lenguaje natural.</p>
                </div>
                <div class="bg-landing-card border border-gray-700 rounded-2xl p-8 text-center hover:-translate-y-2 hover:border-accent hover:shadow-xl hover:shadow-accent/15 transition-all">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-success/20 rounded-2xl text-3xl text-success">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Análisis con IA</h3>
                    <p class="text-gray-400 leading-relaxed">IA que categoriza automáticamente tus gastos.</p>
                </div>
                <div class="bg-landing-card border border-gray-700 rounded-2xl p-8 text-center hover:-translate-y-2 hover:border-accent hover:shadow-xl hover:shadow-accent/15 transition-all">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-accent/20 rounded-2xl text-3xl text-accent">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Dashboard Intuitivo</h3>
                    <p class="text-gray-400 leading-relaxed">Visualiza tu situación financiera con gráficos claros.</p>
                </div>
            </div>
        </section>

        <!-- How it works -->
        <section class="px-6 lg:px-24 py-24">
            <div class="text-center mb-16">
                <h2 class="text-3xl lg:text-4xl font-bold font-display">Comienza en 3 simples pasos</h2>
            </div>
            <div class="flex flex-col lg:flex-row items-center justify-center gap-8">
                <div class="text-center max-w-xs">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-gradient-to-br from-accent to-accent-light rounded-full text-2xl font-bold text-white">1</div>
                    <h3 class="text-xl font-semibold mb-2">Crea tu cuenta</h3>
                    <p class="text-gray-400">Regístrate gratis en menos de un minuto</p>
                </div>
                <div class="w-20 h-0.5 lg:w-0.5 lg:h-20 bg-gradient-to-r lg:bg-gradient-to-b from-accent to-accent-light opacity-50"></div>
                <div class="text-center max-w-xs">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-gradient-to-br from-accent to-accent-light rounded-full text-2xl font-bold text-white">2</div>
                    <h3 class="text-xl font-semibold mb-2">Configura tu perfil</h3>
                    <p class="text-gray-400">Conecta Telegram y configura tu API de Gemini</p>
                </div>
                <div class="w-20 h-0.5 lg:w-0.5 lg:h-20 bg-gradient-to-r lg:bg-gradient-to-b from-accent to-accent-light opacity-50"></div>
                <div class="text-center max-w-xs">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-gradient-to-br from-accent to-accent-light rounded-full text-2xl font-bold text-white">3</div>
                    <h3 class="text-xl font-semibold mb-2">¡Listo!</h3>
                    <p class="text-gray-400">Comienza a registrar gastos y ver tu progreso</p>
                </div>
            </div>
        </section>

        <!-- Free Trial Section -->
        <section class="px-6 lg:px-24 py-24 bg-black/20">
            <div class="max-w-4xl mx-auto text-center">
                <div class="inline-flex items-center gap-2 px-4 py-2 bg-success/15 border border-success/30 rounded-full text-sm text-success mb-6">
                    <i class="fas fa-gift"></i>
                    <span>Prueba Gratuita</span>
                </div>
                <h2 class="text-3xl lg:text-4xl font-bold mb-4 font-display">
                    Prueba el bot <span class="bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">sin compromiso</span>
                </h2>
                <p class="text-lg text-gray-400 leading-relaxed mb-12 max-w-2xl mx-auto">
                    Al registrarte, podrás usar el bot de Telegram con interacciones gratuitas para que pruebes todas las funcionalidades.
                </p>
                <div class="grid sm:grid-cols-3 gap-6 mb-12">
                    <div class="flex flex-col items-center p-6 bg-landing-card border border-gray-700 rounded-2xl hover:-translate-y-1 hover:border-accent transition-all">
                        <div class="w-14 h-14 flex items-center justify-center bg-success/20 rounded-2xl text-2xl text-success mb-4">
                            <i class="fas fa-comments"></i>
                        </div>
                        <h4 class="text-lg font-semibold mb-2">5 Interacciones Gratis</h4>
                        <p class="text-sm text-gray-400">Comienza con 5 interacciones gratuitas</p>
                    </div>
                    <div class="flex flex-col items-center p-6 bg-landing-card border border-gray-700 rounded-2xl hover:-translate-y-1 hover:border-accent transition-all">
                        <div class="w-14 h-14 flex items-center justify-center bg-success/20 rounded-2xl text-2xl text-success mb-4">
                            <i class="fas fa-key"></i>
                        </div>
                        <h4 class="text-lg font-semibold mb-2">API Key Opcional</h4>
                        <p class="text-sm text-gray-400">Configura tu propia API Key para uso ilimitado</p>
                    </div>
                    <div class="flex flex-col items-center p-6 bg-landing-card border border-gray-700 rounded-2xl hover:-translate-y-1 hover:border-accent transition-all">
                        <div class="w-14 h-14 flex items-center justify-center bg-success/20 rounded-2xl text-2xl text-success mb-4">
                            <i class="fas fa-infinity"></i>
                        </div>
                        <h4 class="text-lg font-semibold mb-2">Sin Límites</h4>
                        <p class="text-sm text-gray-400">Con tu API Key, interacciones ilimitadas</p>
                    </div>
                </div>
                <div class="flex justify-center gap-4 flex-wrap">
                    <NuxtLink to="/register" class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-accent to-accent-light text-white rounded-xl font-semibold hover:-translate-y-1 hover:shadow-lg hover:shadow-accent/40 transition-all">
                        <i class="fas fa-rocket"></i>
                        Comenzar Prueba Gratuita
                    </NuxtLink>
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" class="inline-flex items-center gap-2 px-8 py-4 border border-success/50 text-success rounded-xl font-semibold hover:bg-success/10 hover:border-success transition-all">
                        <i class="fas fa-external-link-alt"></i>
                        Obtener API Key Gratis
                    </a>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="px-6 lg:px-24 py-24 bg-gradient-to-br from-accent/10 to-accent-light/5 border-t border-gray-700">
            <div class="text-center">
                <h2 class="text-3xl lg:text-4xl font-bold mb-4 font-display">¿Listo para tomar el control?</h2>
                <p class="text-xl text-gray-400 mb-8">Únete ahora y comienza a gestionar tus finanzas de forma inteligente</p>
                <NuxtLink to="/register" class="inline-flex items-center gap-2 px-10 py-5 bg-gradient-to-r from-accent to-accent-light text-white rounded-xl font-semibold text-lg hover:-translate-y-1 hover:shadow-lg hover:shadow-accent/40 transition-all">
                    <i class="fas fa-user-plus"></i>
                    Crear cuenta gratis
                </NuxtLink>
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
definePageMeta({
    layout: 'public'
})

const { isAuthenticated } = useAuth()

// Redirect authenticated users to dashboard
onMounted(() => {
    if (isAuthenticated.value) {
        navigateTo('/dashboard')
    }
})
</script>

<style scoped>
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}
.animate-float {
    animation: float 6s ease-in-out infinite;
}
.animation-delay-2000 {
    animation-delay: -2s;
}
.animation-delay-4000 {
    animation-delay: -4s;
}
</style>
