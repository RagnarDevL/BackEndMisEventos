# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.models.models import Base
from app.api.routes import router
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils import create_access_token


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],  # Permitir el origen específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir las rutas
app.include_router(router)
# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Aquí deberías verificar el usuario y la contraseña
    print("INFO:", form_data)
    user = {"username": form_data.username}  # Simulación de usuario autenticado
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}