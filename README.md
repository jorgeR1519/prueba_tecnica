# Prueba Técnica: Aplicación con Autenticación + Chat Ollama

## 📋 Descripción

Esta es una aplicación completa que incluye:
- **Backend**: API REST con FastAPI y autenticación JWT
- **Frontend**: Interfaz web con Vue.js 3
- **Chat**: Integración con Ollama para chat con IA (solo usuarios autenticados)

> **Nota**: La aplicación detecta automáticamente si está corriendo en local o Docker y adapta su configuración automáticamente.

---

## 🏗️ Estructura del Proyecto

```
prueba_tecnica/
├── backend/
│   ├── main.py              # Servidor FastAPI
│   ├── auth.py              # Lógica de autenticación JWT
│   ├── models.py            # Modelos Pydantic
│   ├── database/
│   │   └── users.txt        # Base de datos de usuarios
│   ├── requirements.txt     # Dependencias Python
│   └── Dockerfile           # Imagen Docker del backend
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatBox.vue  # Componente de chat con Ollama
│   │   ├── views/
│   │   │   ├── LoginView.vue
│   │   │   └── DashboardView.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── vite.config.js       # Configuración de Vite con proxy
│   ├── nginx.conf           # Configuración de Nginx para Docker
│   └── Dockerfile           # Imagen Docker del frontend
├── docker-compose.yml       # Orquestación de contenedores
└── README.md
```

---

## 🚀 Cómo Ejecutar

### Prerrequisitos

- Python 3.8+ (para desarrollo local)
- Node.js 18+ (para desarrollo local)
- Docker y Docker Compose (opcional, para contenedores)
- Ollama (opcional, para el chat con IA)

### Opción 1: Desarrollo Local (Sin Docker)

#### 1.1 Backend (FastAPI)

```bash
# Navegar al directorio del backend
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv
.\venv\Scripts\activate  # En Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python main.py
```

El backend estará disponible en: `http://localhost:8000`

#### 1.2 Frontend (Vue.js)

```bash
# Navegar al directorio del frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar el servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

### Opción 2: Con Docker

```bash
# En la raíz del proyecto
docker-compose up --build
```

Esto creará:
- Frontend: `http://localhost:80`
- Backend: `http://localhost:8000`

### 3. Ollama (Chat con IA)

La aplicación detecta automáticamente el modelo según el entorno:

#### Para desarrollo local:
```bash
# Instalar Ollama desde https://ollama.ai
# Luego ejecutar:
ollama serve
ollama pull gemma3:4b
```

#### Para Docker:
```bash
# Ollama en Docker requiere menos memoria, usa tinyllama
ollama pull tinyllama
```

**Modelos según entorno:**
| Entorno | Modelo | Memoria |
|---------|--------|---------|
| Local | gemma3:4b | ~4GB |
| Docker | tinyllama | ~700MB |

> **Nota**: El código detecta automáticamente qué modelo usar según el entorno. Si tienes poca memoria, puedes usar `tinyllama` también en local.

---

## 🔐 Cómo Funciona la Validación del Login

### Flujo de Autenticación

1. **Usuario envía credenciales**: El frontend envía email y password al endpoint `/login`
2. **Backend verifica credenciales**: El servidor lee el archivo `database/users.txt`
3. **Validación**: Compara el email y contraseña con los registros del archivo
4. **Generación de token**: Si las credenciales son válidas, genera un token JWT
5. **Respuesta**: Devuelve el token y datos del usuario

### Archivo users.txt

```csv
id,name,email,password
1,Demo User,demo@test.com,Demo123
2,Test User,test@test.com,Test123
3,Admin User,admin@admin.com,Admin123
```

### Endpoints

| Método | Endpoint | Descripción | Autenticado |
|--------|----------|-------------|-------------|
| POST | `/login` | Iniciar sesión | No |
| GET | `/me` | Obtener info del usuario | Sí (JWT) |

### Uso de los Endpoints

**Login:**
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@test.com", "password": "Demo123"}'
```

**Obtener usuario actual:**
```bash
curl -X GET http://localhost:8000/me \
  -H "Authorization: Bearer TU_TOKEN_JWT"
```

---

## 💬 Chat con Ollama

### Características

- Solo accesible para usuarios autenticados
- Integración con Ollama API local (`localhost:11434`)
- Modelo por defecto: `gemma3:4b` (puede cambiarse en el código)
- Historial de conversación persistido durante la sesión

### Configuración

Si Ollama no está disponible, el chat mostrará un mensaje de advertencia pero la aplicación seguirá funcionando para la autenticación.

---

## 📝 Decisiones Técnicas

1. **JWT para autenticación**: Tokens stateless fáciles de validar
2. **Vue 3 Composition API**: Sintaxis moderna y mejor rendimiento
3. **Axios**: Cliente HTTP robusto para las peticiones
4. **Vue Router**: Gestión de rutas con guards para proteger dashboard
5. **CORS configurado**: Permite comunicación entre frontend y backend
6. **Almacenamiento local**: Token guardado en localStorage para persistencia
7. **Detección automática de entorno**: La aplicación detecta si está en local o Docker y adapta:
   - URL de la API del backend
   - Modelo de Ollama a usar
   - Proxy de Nginx para las rutas de API

---

## 👤 Usuarios de Prueba

| Email | Contraseña | Nombre |
|-------|------------|--------|
| demo@test.com | Demo123 | Demo User |
| test@test.com | Test123 | Test User |
| admin@admin.com | Admin123 | Admin User |

---

## 📦 Dependencias

### Backend
- fastapi
- uvicorn
- python-jose[cryptography]
- passlib[bcrypt]
- pydantic

### Frontend
- vue ^3.4.0
- vue-router ^4.2.5
- axios ^1.6.5
- vite ^5.0.0
- @vitejs/plugin-vue ^5.0.0

---

## ✅ Funcionalidades Implementadas

- [x] Login con validación contra archivo .txt
- [x] Generación de tokens JWT
- [x] Endpoint protegido /me
- [x] Dashboard con información del usuario
- [x] Chat con Ollama (solo usuarios logueados)
- [x] Cerrar sesión
- [x] Protección de rutas
- [x] Documentación completa

