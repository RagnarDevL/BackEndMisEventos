
PASOS PARA INSTALAR BAKCEND:

Paso 1: 
Instalar Dependencias
Abre una terminal en tu directorio de trabajo actual tu ruta(c:/xxxx/xxxxxx/BackEndMisEventos).
Instala las dependencias requeridas usando Poetry (ya que tienes un archivo pyproject.toml). Ejecuta el siguiente comando: poetry install

Paso 2:
Ejecutar contenedores del backend, FronEnd y la base de datos con 
docker-compose up -d , si quieres ejecutarlo aparte solo debes eliminar esto del docker-compose.yml el contenedor del FrontEnd 
 frontend:
    build:
      context: ../../frontend/FrontendMisEventos
    ports:
      - "8080:80"
    depends_on:
      - backend

Verificar que los contenedores queden arriba.

Paso 3: 
Configurar la Base de Datos
Verifica la configuración de la base de datos en app/db/database.py para asegurarte de que apunte a la base de datos correcta.
Ejecuta las migraciones de la base de datos para configurar el esquema de la base de datos. Puedes hacer esto ejecutando: poetry run alembic upgrade head
En caso de tener problemas en el back en la raiz se encuentra un archivo que se llama: DatabaseCreatee.txt donde encontrarás los scripts de la creacion de la base de datos 
en este archivo se encuentra el primer INSERT para la creacion del Admin donde puedes cambiar el usuario y la contraseña se encuentra al final de todo el script.
EMAIL:  admin@admin.com
PASS: clavetusdatos

Paso 4:
Ejecutar el backend con python -m uvicorn app.main:app --reload para tener el 
INFO:     Application startup complete.
y con eso tienes los servicios del backend corriendo.


PRUEBAS CON SWAGGER / FASTAPI

En la ejecución te aparece algo como: Uvicorn running on http://127.0.0.1:8000 
con esta url vamos a agregar lo siguiente http://127.0.0.1:8000/docs y tendremos todos los servicios expuestos con su ejemplo de json o params necesarios para su prueba



PARA EJECUTAR LAS PRUEBAS UNITARIAS

En la consola dentro del proyecto ejecutas py.test y empieza a ejecutar las prueba unitarias