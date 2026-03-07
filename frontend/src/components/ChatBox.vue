<template>
  <div class="chat-container">
    <div class="chat-header">
      <h3>💬 Chat con Ollama</h3>
      <span class="status" :class="{ connected: isConnected }">
        {{ isConnected ? 'Conectado' : 'Desconectado' }}
      </span>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div 
        v-for="(message, index) in messages" 
        :key="index"
        class="message"
        :class="{ 'user-message': message.role === 'user', 'assistant-message': message.role === 'assistant' }"
      >
        <div class="message-content">
          <strong>{{ message.role === 'user' ? 'Tú' : 'AI' }}:</strong>
          <p>{{ message.content }}</p>
        </div>
      </div>
      
      <div v-if="isLoading" class="message assistant-message">
        <div class="message-content">
          <strong>AI:</strong>
          <p class="loading">Escribiendo<span class="dots">...</span></p>
        </div>
      </div>
    </div>
    
    <form @submit.prevent="sendMessage" class="chat-input">
      <input 
        v-model="userInput" 
        type="text" 
        placeholder="Escribe tu mensaje..."
        :disabled="isLoading || !isConnected"
      />
      <button type="submit" :disabled="isLoading || !userInput.trim() || !isConnected">
        Enviar
      </button>
    </form>
    
    <div v-if="!isConnected" class="connection-error">
      <p>⚠️ Ollama no está disponible. Asegúrate de tener Ollama ejecutándose en localhost:11434</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import axios from 'axios'

const OLLAMA_URL = 'http://localhost:11434/api/chat'
const MODEL_NAME = 'gemma3:4b'  // Puedes cambiar a otro modelo disponible

const messages = ref([
  {
    role: 'assistant',
    content: '¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?'
  }
])
const userInput = ref('')
const isLoading = ref(false)
const isConnected = ref(false)
const messagesContainer = ref(null)

// Verificar conexión con Ollama al montar el componente
const checkConnection = async () => {
  try {
    const response = await axios.get('http://localhost:11434/api/tags', { timeout: 3000 })
    isConnected.value = response.status === 200
  } catch (error) {
    isConnected.value = false
    console.log('Ollama no disponible:', error.message)
  }
}

// Enviar mensaje a Ollama
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return
  
  const userMessage = userInput.value.trim()
  userInput.value = ''
  
  // Agregar mensaje del usuario
  messages.value.push({
    role: 'user',
    content: userMessage
  })
  
  isLoading.value = true
  await scrollToBottom()
  
  try {
    const response = await axios.post(OLLAMA_URL, {
      model: MODEL_NAME,
      messages: messages.value.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      stream: false
    })
    
    // Agregar respuesta del asistente
    messages.value.push({
      role: 'assistant',
      content: response.data.message.content
    })
  } catch (error) {
    console.error('Error al comunicarse con Ollama:', error)
    messages.value.push({
      role: 'assistant',
      content: 'Lo siento, hubo un error al procesar tu mensaje. Asegúrate de que Ollama esté ejecutándose.'
    })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

// Scroll automático al final
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Verificar conexión periódicamente
onMounted(() => {
  checkConnection()
  // Verificar conexión cada 30 segundos
  setInterval(checkConnection, 30000)
})

// Auto-scroll cuando hay nuevos mensajes
watch(messages.value, () => {
  scrollToBottom()
}, { deep: true })
</script>

<style scoped>
.chat-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 500px;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
}

.status {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
}

.status.connected {
  background: rgba(76, 175, 80, 0.8);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f9f9f9;
}

.message {
  margin-bottom: 16px;
  display: flex;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
}

.user-message {
  justify-content: flex-end;
}

.user-message .message-content {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 4px;
}

.assistant-message {
  justify-content: flex-start;
}

.assistant-message .message-content {
  background: white;
  color: #333;
  border: 1px solid #e0e0e0;
  border-bottom-left-radius: 4px;
}

.message-content strong {
  display: block;
  margin-bottom: 4px;
  font-size: 12px;
}

.message-content p {
  margin: 0;
  line-height: 1.5;
}

.loading {
  color: #666;
}

.dots::after {
  content: '';
  animation: dots 1.5s infinite;
}

@keyframes dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

.chat-input {
  display: flex;
  padding: 16px;
  background: white;
  border-top: 1px solid #e0e0e0;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.chat-input input:focus {
  outline: none;
  border-color: #667eea;
}

.chat-input button {
  padding: 12px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.chat-input button:hover:not(:disabled) {
  background: #5a6fd6;
}

.chat-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.connection-error {
  padding: 12px;
  background: #fff3cd;
  color: #856404;
  text-align: center;
  font-size: 13px;
  border-top: 1px solid #ffeeba;
}
</style>

