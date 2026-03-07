<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="user-info">
        <h1>Bienvenido, {{ user?.name || 'Usuario' }}</h1>
        <p>{{ user?.email }}</p>
      </div>
      <button @click="logout" class="logout-btn">
        Cerrar Sesión
      </button>
    </header>
    
    <main class="dashboard-content">
      <div class="user-card">
        <h2>Información del Usuario</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">ID:</span>
            <span class="value">{{ user?.id }}</span>
          </div>
          <div class="info-item">
            <span class="label">Nombre:</span>
            <span class="value">{{ user?.name }}</span>
          </div>
          <div class="info-item">
            <span class="label">Email:</span>
            <span class="value">{{ user?.email }}</span>
          </div>
        </div>
      </div>
      
      <div class="chat-section">
        <ChatBox />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import ChatBox from '../components/ChatBox.vue'

const router = useRouter()
const user = ref(null)

const API_URL = 'http://localhost:8000'

// Cargar información del usuario
const fetchUserInfo = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  
  try {
    const response = await axios.get(`${API_URL}/me`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    user.value = response.data
    localStorage.setItem('user', JSON.stringify(response.data))
  } catch (error) {
    console.error('Error al obtener usuario:', error)
    // Si el token expiró, redirigir a login
    if (error.response?.status === 401) {
      logout()
    }
  }
}

// Cerrar sesión
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

onMounted(() => {
  // Intentar obtener usuario desde localStorage primero
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
  }
  // Luego actualizar desde el servidor
  fetchUserInfo()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f5f5f5;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.user-info h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 4px;
}

.user-info p {
  color: #666;
  font-size: 14px;
}

.logout-btn {
  padding: 10px 20px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: #da190b;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;
  padding: 24px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.user-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.user-card h2 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #667eea;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item .label {
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item .value {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.chat-section {
  min-width: 0;
}

@media (max-width: 900px) {
  .dashboard-content {
    grid-template-columns: 1fr;
    padding: 16px;
  }
  
  .dashboard-header {
    padding: 16px;
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>

