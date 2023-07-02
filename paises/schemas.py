from pydantic import BaseModel
from typing import List

class Capital(BaseModel):
    capital: str

class Moneda(BaseModel):
    moneda: str

class Continente(BaseModel):
    nombre: str

class Lenguaje(BaseModel):
    lenguaje: str

class Pais(BaseModel):
    id: int
    nombre: str
    poblacion: int
    bandera: str
    capitales: List[Capital] = []
    monedas: List[Moneda] = []
    continentes: List[Continente] = []
    lenguajes: List[Lenguaje] = []

class PaisList(BaseModel):
    paises: List[Pais]
