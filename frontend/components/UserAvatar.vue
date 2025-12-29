<template>
    <div class="user-avatar" :class="sizeClass" :style="avatarStyle">
        <img 
            v-if="imageUrl" 
            :src="fullImageUrl" 
            :alt="displayName"
            @error="handleImageError"
        />
        <span v-else class="initials">{{ initials }}</span>
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

// Size classes
const sizeClass = computed(() => `avatar-${props.size}`)

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

<style scoped>
.user-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
    color: white;
    font-weight: 600;
    text-transform: uppercase;
    user-select: none;
}

.user-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-sm {
    width: 32px;
    height: 32px;
    font-size: 0.75rem;
}

.avatar-md {
    width: 48px;
    height: 48px;
    font-size: 1rem;
}

.avatar-lg {
    width: 72px;
    height: 72px;
    font-size: 1.5rem;
}

.avatar-xl {
    width: 120px;
    height: 120px;
    font-size: 2.5rem;
}

.initials {
    line-height: 1;
}
</style>
