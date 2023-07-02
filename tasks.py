from celery import Celery

from paises.script import obtener_paises_desde_api

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def obtener_paises_async_desde_api():
    print("Ejecutando tarea obtener paises desde api")
    obtener_paises_desde_api()