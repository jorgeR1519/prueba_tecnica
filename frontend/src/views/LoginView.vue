<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Iniciar Sesión</h1>
      <p class="subtitle">Prueba Técnica - Backend + Frontend + Chat Ollama</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            placeholder="Ingresa tu email"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="Ingresa tu contraseña"
            required
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
        </button>
      </form>
      
      <div class="users-info">
        <h3>Usuarios de prueba:</h3>
        <ul>
          <li><strong>demo@test.com</strong> / Demo123</li>
          <li><strong>test@test.com</strong> / Test123</li>
          <li><strong>admin@admin.com</strong> / Admin123</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

// Detectar si estamos en producción (Docker)
const isProduction = window.location.hostname !== 'localhost' && window.location.port !== '5173'
const API_URL = isProduction ? '' : 'http://localhost:8000'

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.post(`${API_URL}/login`, {
      email: email.value,
      password: password.value
    })
    
    // Guardar token y datos del usuario
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    // Redirigir al dashboard
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
}

button {
  width: 100%;
  padding: 14px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #f44336;
  text-align: center;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 6px;
  font-size: 14px;
}

.users-info {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.users-info h3 {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.users-info ul {
  list-style: none;
  font-size: 13px;
  color: #555;
}

.users-info li {
  padding: 4px 0;
}
</style>

