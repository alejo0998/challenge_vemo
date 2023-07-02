import requests
from fastapi import status
from db import session

from paises.models import Capital, Continente, Lenguaje, Moneda, Pais

def get_or_create(model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def obtener_paises_desde_api():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    if response.status_code == status.HTTP_200_OK:
        paises = response.json()
        for pais in paises:
            nombre = pais['name']['official']
            poblacion = pais['population'] if 'population' in pais else None
            bandera = pais['flag']
            capitales = list()
            continentes = list()
            lenguajes = list()
            monedas = list()
            for capital in pais.get('capital') if pais.get('capital') else []:
                capitales.append(get_or_create(Capital, capital=capital))
    
            for continente in pais.get('continents') if pais.get('continents') else []:
                continentes.append(get_or_create(Continente, nombre=continente))
    
            for lenguaje in pais.get('languages').values() if pais.get('languages') else []:
                lenguajes.append(get_or_create(Lenguaje, lenguaje=lenguaje))
            
            for moneda in pais.get('currencies').values() if pais.get('currencies') else []:
                monedas.append(get_or_create(Moneda, moneda=moneda['name']))
    
            datos_pais = {'nombre': nombre, 
                          'poblacion': poblacion,
                          'bandera': bandera, 
                          'capitales': capitales,
                          'lenguajes': lenguajes, 
                          'monedas': monedas , 
                          'continentes': continentes, 
                          'lenguajes': lenguajes
                          }
            crear_pais(datos_pais, datos_pais.get('nombre'))
    else:
        print("Error al obtener los datos de los países desde la API")

def crear_pais(datos_pais, filtro):
    instance = session.query(Pais).filter_by(nombre=filtro).first()
    if instance:
        return instance
    else:
        instance = Pais(**datos_pais)
        session.add(instance)
        session.commit()
        return instance