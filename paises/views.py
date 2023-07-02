from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from .models import Pais as DBPais
from .models import Capital as DBCapital
from .models import Continente as DBContinente
from .schemas import Pais, PaisList, Capital, Moneda, Continente, Lenguaje
from db import Session
import pandas as pd
from fastapi.responses import FileResponse
import tempfile

router = APIRouter(prefix='/api')

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.get("/pais/", response_model=PaisList)
def listar_paises(nombre: str = None, capital: str = None, continente: str = None, order_by: str = None, db: Session = Depends(get_db)):
    paises = get_query_filter_pais(db, nombre, capital, continente, order_by)
    paises_schema = [Pais(id=pais.id, nombre=pais.nombre, poblacion=pais.poblacion, bandera=pais.bandera,
                          capitales=[Capital(capital=c.capital) for c in pais.capitales],
                          monedas=[Moneda(moneda=m.moneda) for m in pais.monedas],
                          continentes=[Continente(nombre=cont.nombre) for cont in pais.continentes],
                          lenguajes=[Lenguaje(lenguaje=l.lenguaje) for l in pais.lenguajes]) for pais in paises]

    return PaisList(paises=paises_schema)

@router.get("/pais/{pais_id}", response_model=Pais)
def obtener_pais(pais_id: int, db: Session = Depends(get_db)):
    pais = db.query(DBPais).filter(DBPais.id == pais_id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    
    pais_schema = Pais(
        id=pais.id,
        nombre=pais.nombre,
        poblacion=pais.poblacion,
        bandera=pais.bandera,
        capitales=[Capital(capital=c.capital) for c in pais.capitales],
        monedas=[Moneda(moneda=m.moneda) for m in pais.monedas],
        continentes=[Continente(nombre=cont.nombre) for cont in pais.continentes],
        lenguajes=[Lenguaje(lenguaje=l.lenguaje) for l in pais.lenguajes]
    )
    
    return pais_schema

@router.get("/pais/download/excel", response_class=FileResponse)
def exportar_paises(nombre: str = None, capital: str = None, continente: str = None, order_by: str = None, db: Session = Depends(get_db)):
    paises = get_query_filter_pais(db, nombre, capital, continente, order_by)
    data = {
        'ID': [pais.id for pais in paises],
        'Nombre': [pais.nombre for pais in paises],
        'Población': [pais.poblacion for pais in paises],
        'Bandera': [pais.bandera for pais in paises],
        'Capitales': [', '.join([c.capital for c in pais.capitales]) for pais in paises],
        'Monedas': [', '.join([m.moneda for m in pais.monedas]) for pais in paises],
        'Continentes': [', '.join([cont.nombre for cont in pais.continentes]) for pais in paises],
        'Lenguajes': [', '.join([l.lenguaje for l in pais.lenguajes]) for pais in paises],
    }
    df = pd.DataFrame(data)

    # Guardar DataFrame en un archivo Excel temporal
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_file:
        filename = tmp_file.name
        df.to_excel(tmp_file.name, index=False, sheet_name='Paises')

    # Devolver el archivo Excel como respuesta
    return FileResponse(filename, filename='paises.xlsx')


def get_query_filter_pais(db, nombre: str = None, capital: str = None, continente: str = None, order_by: str = None):
    query = db.query(DBPais)
    if nombre:
        query = query.filter(DBPais.nombre.ilike(f"%{nombre}%"))
    if capital:
        query = query.filter(DBPais.capitales.any(DBCapital.capital.ilike(f"%{capital}%")))
    if continente:
        query = query.filter(DBPais.continentes.any(DBContinente.nombre.ilike(f"%{continente}%")))

    if order_by:
        if order_by == "nombre":
            query = query.order_by(DBPais.nombre)
        elif order_by == "capital":
            query = query.join(DBPais.capitales).order_by(DBCapital.capital)
        elif order_by == "continente":
            query = query.join(DBPais.continentes).order_by(DBContinente.nombre)
    return query.all()