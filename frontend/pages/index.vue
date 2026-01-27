<template>
    <div class="text-white">
        <!-- Hero Section -->
        <section class="min-h-[calc(100vh-80px)] grid lg:grid-cols-2 gap-16 items-center px-6 lg:px-24 py-16 relative overflow-hidden">
            <!-- Gradient background -->
            <div class="absolute -top-1/2 -right-1/5 w-4/5 h-[150%] bg-[radial-gradient(circle,rgba(147,51,234,0.15)_0%,transparent_70%)] pointer-events-none"></div>
            
            <div class="relative z-10 lg:text-left text-center">
                <div class="inline-flex items-center gap-2 px-4 py-2 bg-accent/15 border border-accent/30 rounded-full text-sm text-accent mb-6">
                    <i class="fas fa-bolt"></i>
                    <span>{{ $t('landing.hero.badge') }}</span>
                </div>
                <h1 class="text-4xl lg:text-6xl font-bold leading-tight mb-6 font-display">
                    {{ $t('landing.hero.title') }}
                    <span class="bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">{{ $t('landing.hero.titleAccent') }}</span>
                </h1>
                <p class="text-lg lg:text-xl text-gray-400 leading-relaxed mb-8 max-w-xl lg:mx-0 mx-auto">
                    {{ $t('landing.hero.subtitle') }}
                </p>
                <div class="flex gap-4 mb-12 flex-wrap lg:justify-start justify-center">
                    <UButton
                        to="/register"
                        icon="i-heroicons-rocket-launch"
                        label="Comenzar ahora"
                        size="xl"
                        class="bg-gradient-to-r from-accent to-accent-light text-white rounded-xl font-semibold hover:-translate-y-1 hover:shadow-lg hover:shadow-accent/40 transition-all"
                    />
                    <UButton
                        to="/login"
                        icon="i-heroicons-arrow-right-start-on-rectangle"
                        label="Iniciar sesión"
                        variant="outline"
                        color="neutral"
                        size="xl"
                        class="border-gray-600 text-white rounded-xl font-semibold hover:bg-white/5 hover:border-accent transition-all"
                    />
                </div>
                <div class="flex items-center gap-8 lg:justify-start justify-center">
                    <div class="text-center">
                        <span class="block text-2xl font-bold">100%</span>
                        <span class="text-sm text-gray-400">{{ $t('landing.hero.stats.free') }}</span>
                    </div>
                    <div class="w-px h-10 bg-gray-600"></div>
                    <div class="text-center">
                        <span class="block text-2xl font-bold text-accent"><i class="fab fa-telegram"></i></span>
                        <span class="text-sm text-gray-400">{{ $t('landing.hero.stats.integration') }}</span>
                    </div>
                    <div class="w-px h-10 bg-gray-600"></div>
                    <div class="text-center">
                        <span class="block text-2xl font-bold text-accent"><i class="fas fa-brain"></i></span>
                        <span class="text-sm text-gray-400">{{ $t('landing.hero.stats.ai') }}</span>
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
                <h2 class="text-3xl lg:text-4xl font-bold mb-4 font-display">{{ $t('landing.features.title') }}</h2>
                <p class="text-lg text-gray-400">{{ $t('landing.features.subtitle') }}</p>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
                <div class="bg-landing-card border border-gray-700 rounded-2xl p-8 text-center hover:-translate-y-2 hover:border-accent hover:shadow-xl hover:shadow-accent/15 transition-all">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-accent/20 rounded-2xl text-3xl text-accent">
                        <i class="fas fa-mobile-alt"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">{{ $t('landing.features.easy.title') }}</h3>
                    <p class="text-gray-400 leading-relaxed">{{ $t('landing.features.easy.description') }}</p>
                </div>
                <div class="bg-landing-card border border-gray-700 rounded-2xl p-8 text-center hover:-translate-y-2 hover:border-accent hover:shadow-xl hover:shadow-accent/15 transition-all">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-[#0088cc]/20 rounded-2xl text-3xl text-[#0088cc]">
                        <i class="fab fa-telegram"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">{{ $t('landing.features.bot.title') }}</h3>
                    <p class="text-gray-400 leading-relaxed">{{ $t('landing.features.bot.description') }}</p>
                </div>
                <div class="bg-landing-card border border-gray-700 rounded-2xl p-8 text-center hover:-translate-y-2 hover:border-accent hover:shadow-xl hover:shadow-accent/15 transition-all">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-success/20 rounded-2xl text-3xl text-success">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">{{ $t('landing.features.ai.title') }}</h3>
                    <p class="text-gray-400 leading-relaxed">{{ $t('landing.features.ai.description') }}</p>
                </div>
                <div class="bg-landing-card border border-gray-700 rounded-2xl p-8 text-center hover:-translate-y-2 hover:border-accent hover:shadow-xl hover:shadow-accent/15 transition-all">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-accent/20 rounded-2xl text-3xl text-accent">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">{{ $t('landing.features.dashboard.title') }}</h3>
                    <p class="text-gray-400 leading-relaxed">{{ $t('landing.features.dashboard.description') }}</p>
                </div>
            </div>
        </section>

        <!-- How it works -->
        <section class="px-6 lg:px-24 py-24">
            <div class="text-center mb-16">
                <h2 class="text-3xl lg:text-4xl font-bold font-display">{{ $t('landing.howItWorks.title') }}</h2>
            </div>
            <div class="flex flex-col lg:flex-row items-center justify-center gap-8">
                <div class="text-center max-w-xs">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-gradient-to-br from-accent to-accent-light rounded-full text-2xl font-bold text-white">1</div>
                    <h3 class="text-xl font-semibold mb-2">{{ $t('landing.howItWorks.step1.title') }}</h3>
                    <p class="text-gray-400">{{ $t('landing.howItWorks.step1.description') }}</p>
                </div>
                <div class="w-20 h-0.5 lg:w-0.5 lg:h-20 bg-gradient-to-r lg:bg-gradient-to-b from-accent to-accent-light opacity-50"></div>
                <div class="text-center max-w-xs">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-gradient-to-br from-accent to-accent-light rounded-full text-2xl font-bold text-white">2</div>
                    <h3 class="text-xl font-semibold mb-2">{{ $t('landing.howItWorks.step2.title') }}</h3>
                    <p class="text-gray-400">{{ $t('landing.howItWorks.step2.description') }}</p>
                </div>
                <div class="w-20 h-0.5 lg:w-0.5 lg:h-20 bg-gradient-to-r lg:bg-gradient-to-b from-accent to-accent-light opacity-50"></div>
                <div class="text-center max-w-xs">
                    <div class="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-gradient-to-br from-accent to-accent-light rounded-full text-2xl font-bold text-white">3</div>
                    <h3 class="text-xl font-semibold mb-2">{{ $t('landing.howItWorks.step3.title') }}</h3>
                    <p class="text-gray-400">{{ $t('landing.howItWorks.step3.description') }}</p>
                </div>
            </div>
        </section>

        <!-- Free Trial Section -->
        <section class="px-6 lg:px-24 py-24 bg-black/20">
            <div class="max-w-4xl mx-auto text-center">
                <div class="inline-flex items-center gap-2 px-4 py-2 bg-success/15 border border-success/30 rounded-full text-sm text-success mb-6">
                    <i class="fas fa-gift"></i>
                    <span>{{ $t('landing.trial.badge') }}</span>
                </div>
                <h2 class="text-3xl lg:text-4xl font-bold mb-4 font-display">
                    {{ $t('landing.trial.title') }} <span class="bg-gradient-to-r from-accent to-accent-light bg-clip-text text-transparent">{{ $t('landing.trial.titleAccent') }}</span>
                </h2>
                <p class="text-lg text-gray-400 leading-relaxed mb-12 max-w-2xl mx-auto">
                    {{ $t('landing.trial.description') }}
                </p>
                <div class="grid sm:grid-cols-3 gap-6 mb-12">
                    <div class="flex flex-col items-center p-6 bg-landing-card border border-gray-700 rounded-2xl hover:-translate-y-1 hover:border-accent transition-all">
                        <div class="w-14 h-14 flex items-center justify-center bg-success/20 rounded-2xl text-2xl text-success mb-4">
                            <i class="fas fa-comments"></i>
                        </div>
                        <h4 class="text-lg font-semibold mb-2">{{ $t('landing.trial.card1.title') }}</h4>
                        <p class="text-sm text-gray-400">{{ $t('landing.trial.card1.description') }}</p>
                    </div>
                    <div class="flex flex-col items-center p-6 bg-landing-card border border-gray-700 rounded-2xl hover:-translate-y-1 hover:border-accent transition-all">
                        <div class="w-14 h-14 flex items-center justify-center bg-success/20 rounded-2xl text-2xl text-success mb-4">
                            <i class="fas fa-key"></i>
                        </div>
                        <h4 class="text-lg font-semibold mb-2">{{ $t('landing.trial.card2.title') }}</h4>
                        <p class="text-sm text-gray-400">{{ $t('landing.trial.card2.description') }}</p>
                    </div>
                    <div class="flex flex-col items-center p-6 bg-landing-card border border-gray-700 rounded-2xl hover:-translate-y-1 hover:border-accent transition-all">
                        <div class="w-14 h-14 flex items-center justify-center bg-success/20 rounded-2xl text-2xl text-success mb-4">
                            <i class="fas fa-infinity"></i>
                        </div>
                        <h4 class="text-lg font-semibold mb-2">{{ $t('landing.trial.card3.title') }}</h4>
                        <p class="text-sm text-gray-400">{{ $t('landing.trial.card3.description') }}</p>
                    </div>
                </div>
                <div class="flex justify-center gap-4 flex-wrap">
                    <UButton
                        to="/register"
                        icon="i-heroicons-rocket-launch"
                        label="Empezar ahora"
                        size="xl"
                        class="bg-gradient-to-r from-accent to-accent-light text-white rounded-xl font-semibold hover:-translate-y-1 hover:shadow-lg hover:shadow-accent/40 transition-all"
                    />
                    <UButton
                        href="https://aistudio.google.com/app/apikey"
                        target="_blank"
                        icon="i-heroicons-arrow-top-right-on-square"
                        label="Obtener API Key"
                        variant="outline"
                        color="success"
                        size="xl"
                        class="border-success/50 text-success rounded-xl font-semibold hover:bg-success/10 hover:border-success transition-all"
                    />
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="px-6 lg:px-24 py-24 bg-gradient-to-br from-accent/10 to-accent-light/5 border-t border-gray-700">
            <div class="text-center">
                <h2 class="text-3xl lg:text-4xl font-bold mb-4 font-display">{{ $t('landing.cta.title') }}</h2>
                <p class="text-xl text-gray-400 mb-8">{{ $t('landing.cta.subtitle') }}</p>
                <UButton
                    to="/register"
                    icon="i-heroicons-user-plus"
                    label="Crear cuenta gratis"
                    size="xl"
                    class="bg-gradient-to-r from-accent to-accent-light text-white rounded-xl font-semibold text-lg hover:-translate-y-1 hover:shadow-lg hover:shadow-accent/40 transition-all px-10 py-5"
                />
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
