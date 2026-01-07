<template>
    <div class="landing-page">
        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-content">
                <div class="hero-badge">
                    <i class="fas fa-bolt"></i>
                    <span>Gestión financiera inteligente</span>
                </div>
                <h1 class="hero-title">
                    Toma el control de tus
                    <span class="gradient-text">finanzas personales</span>
                </h1>
                <p class="hero-description">
                    Registra gastos con facilidad, analiza tus hábitos financieros y alcanza tus metas de ahorro. 
                    Todo en un solo lugar, con la ayuda de inteligencia artificial.
                </p>
                <div class="hero-cta">
                    <NuxtLink to="/register" class="btn-primary">
                        <i class="fas fa-rocket"></i>
                        Comenzar Gratis
                    </NuxtLink>
                    <NuxtLink to="/login" class="btn-secondary">
                        <i class="fas fa-sign-in-alt"></i>
                        Ya tengo cuenta
                    </NuxtLink>
                </div>
                <div class="hero-stats">
                    <div class="stat">
                        <span class="stat-value">100%</span>
                        <span class="stat-label">Gratis</span>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="stat">
                        <span class="stat-value"><i class="fab fa-telegram"></i></span>
                        <span class="stat-label">Integración</span>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="stat">
                        <span class="stat-value"><i class="fas fa-brain"></i></span>
                        <span class="stat-label">Con IA</span>
                    </div>
                </div>
            </div>
            <div class="hero-visual">
                <div class="floating-card card-1">
                    <i class="fas fa-arrow-up text-success"></i>
                    <span>+$250,000</span>
                    <small>Ingreso registrado</small>
                </div>
                <div class="floating-card card-2">
                    <i class="fas fa-chart-pie"></i>
                    <span>Análisis</span>
                    <small>En tiempo real</small>
                </div>
                <div class="floating-card card-3">
                    <i class="fas fa-piggy-bank text-primary"></i>
                    <span>Meta: 80%</span>
                    <small>Ahorro mensual</small>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features">
            <div class="features-header">
                <h2>Todo lo que necesitas para gestionar tu dinero</h2>
                <p>Herramientas poderosas diseñadas para simplificar tu vida financiera</p>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-mobile-alt"></i>
                    </div>
                    <h3>Registro Fácil</h3>
                    <p>Registra tus gastos e ingresos en segundos desde cualquier dispositivo. Interfaz intuitiva y rápida.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon telegram">
                        <i class="fab fa-telegram"></i>
                    </div>
                    <h3>Bot de Telegram</h3>
                    <p>Registra gastos directamente desde Telegram con lenguaje natural. Solo escribe "Gasté $50 en almuerzo".</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon ai">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3>Análisis con IA</h3>
                    <p>Inteligencia artificial que categoriza automáticamente tus gastos y te brinda insights personalizados.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3>Dashboard Intuitivo</h3>
                    <p>Visualiza tu situación financiera con gráficos claros. Entiende a dónde va tu dinero de un vistazo.</p>
                </div>
            </div>
        </section>

        <!-- How it works -->
        <section class="how-it-works">
            <div class="how-header">
                <h2>Comienza en 3 simples pasos</h2>
            </div>
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>Crea tu cuenta</h3>
                    <p>Regístrate gratis en menos de un minuto</p>
                </div>
                <div class="step-connector"></div>
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>Configura tu perfil</h3>
                    <p>Conecta Telegram y configura tu API de Gemini</p>
                </div>
                <div class="step-connector"></div>
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>¡Listo!</h3>
                    <p>Comienza a registrar gastos y ver tu progreso</p>
                </div>
            </div>
        </section>

        <!-- Free Trial Section -->
        <section class="free-trial">
            <div class="free-trial-content">
                <div class="free-trial-badge">
                    <i class="fas fa-gift"></i>
                    <span>Prueba Gratuita</span>
                </div>
                <h2>Prueba el bot <span class="gradient-text">sin compromiso</span></h2>
                <p class="free-trial-description">
                    Al registrarte, podrás usar el bot de Telegram con interacciones gratuitas para que pruebes 
                    todas las funcionalidades. ¡Sin necesidad de configurar nada adicional!
                </p>
                <div class="trial-features">
                    <div class="trial-feature">
                        <div class="trial-icon">
                            <i class="fas fa-comments"></i>
                        </div>
                        <div class="trial-info">
                            <h4>5 Interacciones Gratis</h4>
                            <p>Comienza con 5 interacciones gratuitas para probar el sistema</p>
                        </div>
                    </div>
                    <div class="trial-feature">
                        <div class="trial-icon">
                            <i class="fas fa-key"></i>
                        </div>
                        <div class="trial-info">
                            <h4>API Key Opcional</h4>
                            <p>Configura tu propia API Key de Gemini (gratis) para uso ilimitado</p>
                        </div>
                    </div>
                    <div class="trial-feature">
                        <div class="trial-icon">
                            <i class="fas fa-infinity"></i>
                        </div>
                        <div class="trial-info">
                            <h4>Sin Límites</h4>
                            <p>Con tu propia API Key, disfruta de interacciones ilimitadas</p>
                        </div>
                    </div>
                </div>
                <div class="trial-cta">
                    <NuxtLink to="/register" class="btn-primary">
                        <i class="fas fa-rocket"></i>
                        Comenzar Prueba Gratuita
                    </NuxtLink>
                    <a href="https://aistudio.google.com/app/apikey" target="_blank" class="btn-outline">
                        <i class="fas fa-external-link-alt"></i>
                        Obtener API Key Gratis
                    </a>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="cta-section">
            <div class="cta-content">
                <h2>¿Listo para tomar el control?</h2>
                <p>Únete ahora y comienza a gestionar tus finanzas de forma inteligente</p>
                <NuxtLink to="/register" class="btn-primary large">
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
.landing-page {
    color: var(--text-primary);
}

/* Hero Section */
.hero {
    min-height: calc(100vh - 80px);
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
    padding: 4rem 6rem;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 80%;
    height: 150%;
    background: radial-gradient(circle, rgba(147, 51, 234, 0.15) 0%, transparent 70%);
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(147, 51, 234, 0.15);
    border: 1px solid rgba(147, 51, 234, 0.3);
    border-radius: 50px;
    font-size: 0.875rem;
    color: var(--accent-primary);
    margin-bottom: 1.5rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1.5rem;
    font-family: 'Outfit', sans-serif;
}

.gradient-text {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-description {
    font-size: 1.25rem;
    color: var(--text-secondary);
    line-height: 1.7;
    margin-bottom: 2rem;
    max-width: 540px;
}

.hero-cta {
    display: flex;
    gap: 1rem;
    margin-bottom: 3rem;
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    color: white;
    text-decoration: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(147, 51, 234, 0.4);
}

.btn-primary.large {
    padding: 1.25rem 2.5rem;
    font-size: 1.125rem;
}

.btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    background: transparent;
    color: var(--text-primary);
    text-decoration: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1rem;
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.btn-secondary:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: var(--accent-primary);
}

.hero-stats {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.stat {
    text-align: center;
}

.stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
}

.stat-value i {
    font-size: 1.75rem;
    color: var(--accent-primary);
}

.stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.stat-divider {
    width: 1px;
    height: 40px;
    background: var(--border-color);
}

/* Hero Visual */
.hero-visual {
    position: relative;
    height: 500px;
}

.floating-card {
    position: absolute;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    animation: float 6s ease-in-out infinite;
}

.floating-card i {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.floating-card span {
    display: block;
    font-weight: 600;
    font-size: 1.125rem;
}

.floating-card small {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.card-1 {
    top: 10%;
    right: 20%;
    animation-delay: 0s;
}

.card-2 {
    top: 40%;
    right: 5%;
    animation-delay: -2s;
}

.card-3 {
    bottom: 15%;
    right: 25%;
    animation-delay: -4s;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Features Section */
.features {
    padding: 6rem;
    background: rgba(0, 0, 0, 0.2);
}

.features-header {
    text-align: center;
    margin-bottom: 4rem;
}

.features-header h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    font-family: 'Outfit', sans-serif;
}

.features-header p {
    font-size: 1.125rem;
    color: var(--text-secondary);
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
}

.feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-8px);
    border-color: var(--accent-primary);
    box-shadow: 0 20px 40px rgba(147, 51, 234, 0.15);
}

.feature-icon {
    width: 70px;
    height: 70px;
    margin: 0 auto 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(147, 51, 234, 0.2), rgba(168, 85, 247, 0.1));
    border-radius: 20px;
    font-size: 1.75rem;
    color: var(--accent-primary);
}

.feature-icon.telegram {
    background: linear-gradient(135deg, rgba(0, 136, 204, 0.2), rgba(0, 136, 204, 0.1));
    color: #0088cc;
}

.feature-icon.ai {
    background: linear-gradient(135deg, rgba(76, 225, 182, 0.2), rgba(76, 225, 182, 0.1));
    color: #4CE1B6;
}

.feature-card h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
}

.feature-card p {
    color: var(--text-secondary);
    line-height: 1.6;
}

/* How it works */
.how-it-works {
    padding: 6rem;
}

.how-header {
    text-align: center;
    margin-bottom: 4rem;
}

.how-header h2 {
    font-size: 2.5rem;
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
}

.steps {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
}

.step {
    text-align: center;
    max-width: 250px;
}

.step-number {
    width: 60px;
    height: 60px;
    margin: 0 auto 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    border-radius: 50%;
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
}

.step h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.step p {
    color: var(--text-secondary);
}

.step-connector {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
    opacity: 0.5;
}

/* Free Trial Section */
.free-trial {
    padding: 6rem;
    background: rgba(0, 0, 0, 0.2);
}

.free-trial-content {
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
}

.free-trial-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(76, 225, 182, 0.15);
    border: 1px solid rgba(76, 225, 182, 0.3);
    border-radius: 50px;
    font-size: 0.875rem;
    color: #4CE1B6;
    margin-bottom: 1.5rem;
}

.free-trial h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    font-family: 'Outfit', sans-serif;
}

.free-trial-description {
    font-size: 1.125rem;
    color: var(--text-secondary);
    line-height: 1.7;
    margin-bottom: 3rem;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

.trial-features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-bottom: 3rem;
}

.trial-feature {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 1.5rem;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    transition: all 0.3s ease;
}

.trial-feature:hover {
    transform: translateY(-5px);
    border-color: var(--accent-primary);
}

.trial-icon {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(76, 225, 182, 0.2), rgba(76, 225, 182, 0.1));
    border-radius: 16px;
    font-size: 1.5rem;
    color: #4CE1B6;
    margin-bottom: 1rem;
}

.trial-info h4 {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.trial-info p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    line-height: 1.5;
}

.trial-cta {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.btn-outline {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    background: transparent;
    color: #4CE1B6;
    text-decoration: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1rem;
    border: 1px solid rgba(76, 225, 182, 0.5);
    transition: all 0.3s ease;
}

.btn-outline:hover {
    background: rgba(76, 225, 182, 0.1);
    border-color: #4CE1B6;
}

/* CTA Section */
.cta-section {
    padding: 6rem;
    background: linear-gradient(135deg, rgba(147, 51, 234, 0.1), rgba(168, 85, 247, 0.05));
    border-top: 1px solid var(--border-color);
}

.cta-content {
    text-align: center;
}

.cta-content h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    font-family: 'Outfit', sans-serif;
}

.cta-content p {
    font-size: 1.25rem;
    color: var(--text-secondary);
    margin-bottom: 2rem;
}

/* Text colors */
.text-success {
    color: #4CE1B6;
}

.text-primary {
    color: var(--accent-primary);
}

/* Responsive */
@media (max-width: 1200px) {
    .features-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 992px) {
    .hero {
        grid-template-columns: 1fr;
        padding: 3rem 2rem;
        text-align: center;
    }
    
    .hero-title {
        font-size: 2.5rem;
    }
    
    .hero-description {
        margin: 0 auto 2rem;
    }
    
    .hero-cta {
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .hero-stats {
        justify-content: center;
    }
    
    .hero-visual {
        display: none;
    }
    
    .features, .how-it-works, .cta-section, .free-trial {
        padding: 4rem 2rem;
    }
    
    .trial-features {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .steps {
        flex-direction: column;
    }
    
    .step-connector {
        width: 2px;
        height: 40px;
    }
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
    
    .hero-cta {
        flex-direction: column;
        align-items: stretch;
    }
    
    .btn-primary, .btn-secondary {
        justify-content: center;
    }
}
</style>
