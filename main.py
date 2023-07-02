from fastapi import FastAPI
from paises.views import router as paises_router
from tasks import obtener_paises_async_desde_api
from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
app.include_router(paises_router)


# Configurar Celery
celery_app = Celery('tasks', broker=os.getenv('CELERY_BROKER'), backend=os.getenv('CELERY_BACKEND'))

@app.get("/")
async def enviar_tarea():
    tarea = obtener_paises_async_desde_api.delay()
    return {"task_id": tarea.id}


celery_app.conf.beat_schedule = {
    'obtener_paises': {
        'task': 'tasks.obtener_paises_async_desde_api',
        'schedule': int(os.getenv('SCHEDULE', 60*60*24)),  # Ejecutar cada 15 segundos
    },
}
celery_app.conf.timezone = 'UTC'

celery_app.worker_main(['worker', '--loglevel=info', '-B'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
