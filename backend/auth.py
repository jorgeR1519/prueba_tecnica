import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from models import User

# Configuración
SECRET_KEY = "supersecretkey123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ruta al archivo de usuarios
USERS_FILE = os.path.join(os.path.dirname(__file__), "database", "users.txt")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def read_users_from_file() -> list[dict]:
    """Lee el archivo de usuarios y retorna una lista de diccionarios"""
    users = []
    try:
        with open(USERS_FILE, "r") as f:
            lines = f.readlines()
            # Saltar la primera línea (encabezado)
            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) >= 4:
                    users.append({
                        "id": int(parts[0]),
                        "name": parts[1],
                        "email": parts[2],
                        "password": parts[3]
                    })
    except FileNotFoundError:
        print(f"Archivo no encontrado: {USERS_FILE}")
    return users


def authenticate_user(email: str, password: str) -> Optional[User]:
    """Autentica un usuario contra el archivo .txt"""
    users = read_users_from_file()
    for user_data in users:
        if user_data["email"] == email and user_data["password"] == password:
            return User(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"]
            )
    return None


def get_user_from_token(token: str) -> Optional[User]:
    """Obtiene el usuario desde un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    
    users = read_users_from_file()
    for user_data in users:
        if user_data["email"] == email:
            return User(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"]
            )
    return None

