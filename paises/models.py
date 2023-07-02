from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from db import Base, engine

# Tabla intermedia para la relación muchos a muchos entre Pais y Moneda
pais_moneda = Table(
    "pais_moneda",
    Base.metadata,
    Column("pais_id", Integer, ForeignKey("paises.id")),
    Column("moneda_id", Integer, ForeignKey("monedas.id"))
)

# Tabla intermedia para la relación muchos a muchos entre Pais y Continente
pais_continente = Table(
    "pais_continente",
    Base.metadata,
    Column("pais_id", Integer, ForeignKey("paises.id")),
    Column("continente_id", Integer, ForeignKey("continentes.id"))
)

# Tabla intermedia para la relación muchos a muchos entre Pais y Lenguaje
pais_lenguaje = Table(
    "pais_lenguaje",
    Base.metadata,
    Column("pais_id", Integer, ForeignKey("paises.id")),
    Column("lenguaje_id", Integer, ForeignKey("lenguajes.id"))
)

class Pais(Base):
    __tablename__ = "paises"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    poblacion = Column(Integer)
    bandera = Column(String, unique=True)

    capitales = relationship("Capital", back_populates="pais")
    monedas = relationship("Moneda", secondary=pais_moneda, back_populates="paises")
    continentes = relationship("Continente", secondary=pais_continente, back_populates="paises")
    lenguajes = relationship("Lenguaje", secondary=pais_lenguaje, back_populates="paises")


class Capital(Base):
    __tablename__ = "capitales"

    id = Column(Integer, primary_key=True, index=True)
    capital = Column(String, unique=True)
    pais_id = Column(Integer, ForeignKey("paises.id"))
    pais = relationship("Pais", back_populates="capitales")

class Moneda(Base):
    __tablename__ = "monedas"

    id = Column(Integer, primary_key=True, index=True)
    moneda = Column(String, unique=True)
    paises = relationship("Pais", secondary=pais_moneda, back_populates="monedas")

class Continente(Base):
    __tablename__ = "continentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    paises = relationship("Pais", secondary=pais_continente, back_populates="continentes")

class Lenguaje(Base):
    __tablename__ = "lenguajes"

    id = Column(Integer, primary_key=True, index=True)
    lenguaje = Column(String, unique=True)
    paises = relationship("Pais", secondary=pais_lenguaje, back_populates="lenguajes")

Base.metadata.create_all(bind=engine)
