<template>
    <div 
        class="flex items-center justify-center rounded-full overflow-hidden flex-shrink-0 text-white font-semibold uppercase select-none"
        :class="sizeClasses"
        :style="avatarStyle"
    >
        <img 
            v-if="imageUrl && !imageError" 
            :src="fullImageUrl" 
            :alt="displayName"
            class="w-full h-full object-cover"
            @error="handleImageError"
        />
        <span v-else class="leading-none">{{ initials }}</span>
    </div>
</template>

<script setup lang="ts">
interface Props {
    imageUrl?: string | null
    name?: string | null
    username?: string
    size?: 'sm' | 'md' | 'lg' | 'xl'
}

const props = withDefaults(defineProps<Props>(), {
    imageUrl: null,
    name: null,
    username: '',
    size: 'md'
})

const config = useRuntimeConfig()
const imageError = ref(false)

// Compute the display name for initials
const displayName = computed(() => {
    return props.name || props.username || 'U'
})

// Generate initials from name or username
const initials = computed(() => {
    const name = displayName.value.trim()
    if (!name) return 'U'
    
    const parts = name.split(/\s+/)
    if (parts.length >= 2) {
        // Get first letter of first and last word
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
    }
    // Just use first 1-2 characters of single word
    return name.substring(0, 2).toUpperCase()
})

// Generate consistent color from name
const backgroundColor = computed(() => {
    const colors = [
        '#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e',
        '#16a085', '#27ae60', '#2980b9', '#8e44ad', '#2c3e50',
        '#f1c40f', '#e67e22', '#e74c3c', '#00bcd4', '#673ab7',
        '#ff5722', '#795548', '#607d8b', '#009688', '#3f51b5'
    ]
    
    // Simple hash function based on name
    const name = displayName.value
    let hash = 0
    for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash)
    }
    
    return colors[Math.abs(hash) % colors.length]
})

// Size classes using Tailwind
const sizeClasses = computed(() => {
    const sizes: Record<string, string> = {
        sm: 'w-8 h-8 text-xs',
        md: 'w-12 h-12 text-base',
        lg: 'w-[72px] h-[72px] text-2xl',
        xl: 'w-[120px] h-[120px] text-4xl'
    }
    return sizes[props.size] || sizes.md
})

// Avatar style when showing initials
const avatarStyle = computed(() => {
    if (props.imageUrl && !imageError.value) return {}
    return {
        backgroundColor: backgroundColor.value
    }
})

// Full image URL with API base
const fullImageUrl = computed(() => {
    if (!props.imageUrl) return ''
    // If it's already a full URL, use it directly
    if (props.imageUrl.startsWith('http')) return props.imageUrl
    // Otherwise prepend the API URL
    return `${config.public.apiUrl}${props.imageUrl}`
})

// Handle image load error - fallback to initials
const handleImageError = () => {
    imageError.value = true
}
</script>
