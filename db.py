# db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configuración de la base de datos
DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

# Crea el motor de base de datos
engine = create_engine(DATABASE_URL)

# Crea una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Declarative base para definir los modelos
Base = declarative_base()
