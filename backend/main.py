from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta

from models import UserLogin, Token, UserResponse, User
from auth import (
    authenticate_user,
    create_access_token,
    get_user_from_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="API de Autenticación", description="Backend con autenticación JWT")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bearer token para autenticación
security = HTTPBearer()


@app.get("/")
def root():
    """Endpoint de prueba"""
    return {"message": "API de Autenticación funcionando", "status": "OK"}


@app.post("/login", response_model=Token)
def login(user_login: UserLogin):
    """
    Endpoint de login
    - Recibe email y password
    - Valida contra archivo users.txt
    - Retorna token JWT si es válido
    """
    user = authenticate_user(user_login.email, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Dependencia para obtener el usuario actual desde el token"""
    token = credentials.credentials
    user = get_user_from_token(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@app.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Endpoint protegido que retorna información del usuario autenticado
    Requiere token JWT válido en el header Authorization
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

