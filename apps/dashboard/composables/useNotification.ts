// Using Nuxt UI's toast which is already configured and working
export const useNotification = () => {
  const toast = useToast()

  const success = (title: string, description?: string) => {
    toast.add({
      title,
      description,
      color: 'green',
      icon: 'i-heroicons-check-circle',
    })
  }

  const error = (title: string, description?: string) => {
    toast.add({
      title,
      description,
      color: 'red',
      icon: 'i-heroicons-x-circle',
    })
  }

  const info = (title: string, description?: string) => {
    toast.add({
      title,
      description,
      color: 'blue',
      icon: 'i-heroicons-information-circle',
    })
  }

  const warning = (title: string, description?: string) => {
    toast.add({
      title,
      description,
      color: 'yellow',
      icon: 'i-heroicons-exclamation-triangle',
    })
  }

  const loading = (title: string, description?: string) => {
    return toast.add({
      title,
      description,
      color: 'gray',
      icon: 'i-heroicons-arrow-path',
    })
  }

  const dismiss = (id: string | number) => {
    // Nuxt UI toast doesn't have dismiss by ID, we just clear all
    toast.clear()
  }

  return {
    success,
    error,
    info,
    warning,
    loading,
    dismiss,
    toast,
  }
}
