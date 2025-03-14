from sqlmodel import SQLModel, Field, create_engine, Session

# Definición del modelo
class Usuarios(SQLModel, table=True):
    idUser: int = Field(default=None, primary_key=True)
    Username: str
    MailUser: str
    PassUser: str
    RolUser: str

# Crear una base de datos SQLite
engine = create_engine("sqlite:///database.db")

# Crear las tablas en la base de datos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Insertar datos en la base de datos
def insert_data():
    with Session(engine) as session:
        Usuarios1 = Usuarios(Username="KevinLeon", MailUser="djkleon1992@gmail.com", PassUser="Contraseña**", RolUser="Admin")
        
        session.add(Usuarios1)
        session.commit()

# Consultar datos en la base de datos
def query_data():
    with Session(engine) as session:
        UsuariosList = session.exec(Usuarios.select()).all()  # Usar session.exec() en lugar de session.query()
        for item in UsuariosList:
            print(f"ID: {item.idUser}, Name: {item.Username}, Description: {item.MailUser}")

# Ejecutar las funciones
create_db_and_tables()  # Crear la base de datos y las tablas
insert_data()           # Inserta datos
query_data()            # Consulta e imprime los datos