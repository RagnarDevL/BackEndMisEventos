# app/utils.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.models import User
from app.schemas import UserCreate, UserOut
from passlib.context import CryptContext # type: ignore
from jose import JWTError, jwt
from app.config import settings  # Importa la configuración
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Cambia a "login"

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Convertir la clave en un hash
def hash_password_in(password: str) -> str:
    return pwd_context.hash(password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def get_user_hash(db: Session, username: str):
    user = db.query(User).filter(User.email == username).first()
    return user.password if user else None

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# Función para obtener el usuario
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Función para obtener el usuario
def get_user_email(db: Session, email: int):
    return db.query(User).filter(User.email == email).first()

# Función para autenticar al usuario
def authenticate_user(db: Session, email: str, password: str):
    hashhh = get_user_hash(db, email)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print("Usuario no encontrado")
        return False
    # Imprime el hash almacenado
    if not verify_password(password, user.password):
        print("La contraseña es incorrecta")
        return False

    return user


# Dependencia para obtener el usuario actual
def get_current_user2(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    decoded_token = verify_token(token)  # Verifica el token
    email = decoded_token.get("sub")  # Asegúrate de que esto sea un entero
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    try:
        email = email  # Asegúrate de que esto sea un entero
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID format")

    user = get_user_email(db, email)
    print("DECODEEEEEEE:",user.rol)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user
# Dependencia para obtener el usuario actual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    decoded_token = verify_token(token)  # Verifica el token
    user_id = decoded_token.get("sub")  # Asegúrate de que esto sea un entero
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    try:
        user_id = int(user_id)  # Asegúrate de que esto sea un entero
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID format")

    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        # Decodifica el token usando la clave secreta y el algoritmo
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("VERIFY TOKENNNN",payload)

        return payload  # Devuelve el contenido del token (por ejemplo, el user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")