from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base

app = FastAPI()

# Definir modelo de datos con SQLAlchemy
Base = declarative_base()

class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), index=True)
    autor = Column(String(255))
    paginas = Column(Integer)
    editorial = Column(String(255), nullable=True)

# Configurar conexión a la base de datos MySQL
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/tu_base_de_datos"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Configurar sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo Pydantic para la entrada del libro
class LibroCreate(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: str

@app.post("/libros")
def insertar_libro(libro: LibroCreate):
    # Convertir el modelo Pydantic a modelo SQLAlchemy
    nuevo_libro = Libro(**libro.dict())

    # Insertar el libro en la base de datos
    db = SessionLocal()
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    db.close()

    # Devolver la respuesta
    return {"message": f"Libro {nuevo_libro.titulo} insertado"}






