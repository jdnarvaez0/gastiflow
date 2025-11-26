<template>
  <div>
    <!-- Sidebar -->
    <nav class="sidebar">
        <div class="logo">
            <i class="fa-solid fa-wallet"></i> Gastiflow
        </div>
        <ul class="nav-links">
            <li><NuxtLink to="/" active-class="active"><i class="fa-solid fa-chart-pie"></i> Dashboard</NuxtLink></li>
            <li><a href="#"><i class="fa-solid fa-list"></i> Movimientos</a></li>
            <li><a href="#"><i class="fa-solid fa-chart-line"></i> Reportes</a></li>
            <li><a href="#"><i class="fa-solid fa-credit-card"></i> Cuentas</a></li>
            <li><a href="#"><i class="fa-solid fa-tags"></i> Categorías</a></li>
        </ul>
        
        <div class="sidebar-footer">
            <ul class="nav-links">
                <li><a href="#"><i class="fa-solid fa-gear"></i> Ajustes</a></li>
                <li><a href="#"><i class="fa-solid fa-right-from-bracket"></i> Cerrar sesión</a></li>
            </ul>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
        <slot />
    </main>
  </div>
</template>
