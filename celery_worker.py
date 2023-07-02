from main import celery_app
celery_app.worker_main(['worker', '--loglevel=info', '-B'])
