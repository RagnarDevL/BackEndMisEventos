import pytest
from fastapi.testclient import TestClient
from app.main import app  # Asegúrate de que este importe apunte al archivo principal donde tienes la app FastAPI

client = TestClient(app)

def test_create_user():
    # Datos de prueba
    test_user = {
        "email": "test@example.com",
        "name": "Kevin",
        "password": "testpassword",
        "rol": "user"
    }
    
    # Hacer la solicitud POST al endpoint
    response = client.post("/userCreate/", json=test_user)
    
    # Comprobar que la respuesta sea exitosa
    assert response.status_code == 201  # Assuming the user creation returns 201 Created

    data = response.json()
    
    # Verificar que los datos devueltos coincidan
    assert data["email"] == test_user["email"]
    assert data["name"] == test_user["name"]
    assert "password" not in data  # El password no debe devolverse
    assert data["rol"] == test_user["rol"]

def test_create_user_email_already_registered():
    # Datos de prueba (mismo email para probar el caso de error)
    test_user = {
        "email": "test@example.com",
        "name": "Kevin",
        "password": "testpassword",
        "rol": "user"
    }
    
    # Crear el usuario por primera vez
    client.post("/userCreate/", json=test_user)
    
    # Intentar crearlo de nuevo con el mismo email
    response = client.post("/userCreate/", json=test_user)
    
    # Comprobar que se lanza el error esperado
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
