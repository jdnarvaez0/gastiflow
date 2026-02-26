<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
    <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-primary" />
  </div>
</template>

<script setup>
// Dashboard root - redirect to login or dashboard based on auth
definePageMeta({
  middleware: 'auth'
})

// This will be handled by the auth middleware
// If not authenticated -> redirect to /login
// If authenticated -> redirect to /dashboard
</script>
