# challenge_vemo
Guia para ejecutar el proyecto

* Para iniciar el proyecto hay que crear un virtual environment para instalar las dependencias necesarias.

Dentro de la carpeta del proyecto ejecutar 

python3 -m venv venv

Luego ejecutar para instalar las dependencias necesarias

pip install -r requirements.txt 

Luego ejecutar el siguiente comando para crear dejar ejecutando postgres y redis.

docker-compose up --build


Respecto a la solucion. 
En cuanto al modelado de datos, defini un Pais el cual tiene nombre, poblacion y bandera.
Y cada pais puede tener varias capitales, varias monedas, varios continentes y varios lenguajes.
Donde cada uno de estos son objetos y existen tablas intermedias.
Para todo esto ya esta creada una migration que se ejecuta con
alembic upgrade head


Respecto a los endpoints para obtener los paises, con filtros y demas, se les pega con la siguiente estructura

http://localhost:8000/api/pais/ -> Me trae una lista de todos los paises

http://localhost:8000/api/pais/1 -> Me trae el pais con id uno //Entiendo que al ser paises no hay ninguna restriccion con usar el id, en caso de que sea algo mas critico respecto a seguridad utilizaria un UUID

http://localhost:8000/api/pais/?order_by=nombre -> Me trae los paises y ordena por nombre

http://localhost:8000/api/pais/?continente=Asia -> Me trae todos los paises de asia

http://localhost:8000/api/pais/?continente=Asia&&order_by=nombre -> Me trae todos los paises de asia ordenados por nombre.

http://localhost:8000/api/pais/?continente=Asia&&order_by=nombre -> Me trae todos los paises de asia ordenados por nombre.

localhost:8000/api/pais/download/excel/?continente=Asia -> Este endpoint es para descargar un excel con todos los paises de Asia, funciona con filtros y sin filtros.

Ahora respecto al script que nos da los datos de los paises.
Para este requerimiento utilice Celery para ejecutar las tareas asincronas y redis como worker.
Lo que esta haciendo Celery es ejecutar esa tarea programada cada 12 horas, y cargar los paises en la base de datos. Unicamente esta cargando los nuevos datos, esto es por una cuestion de tiempo, si tuviese mas margen de tiempo haria los updates en los casos que haya cambios, en algun pais.

celery -A celery_worker worker --loglevel=info -> Ejecutamos este comando para dejar corriendo celery, en el directorio raiz. 


Respecto a lo que es la cache, utilice como cache a redis, donde lo setie en 25 horas. Por lo cual cada 25 horas va a volver a consumir el endpoint externo. Mientras, devuelve los datos que ya tenemos cacheados.

Despues respecto a los puntos opcionales, por una cuestion de tiempo no los puedo resolver.

1. Agrega rutas de actividades que se puedan hacer en cada país.
2. Envía un correo electrónico diario con el excel de los datos filtrados por país.

Pero para el punto 1, agregaria otro endpoint donde le pasaria el pais y le pediria las actividades y esto me devolveria una lista de lo que tenga disponible. Estas actividades estimo que las cargaria del endpoint externo utilizado anteriormente.PO2
Para el punto 2, ya existe la generacion del excel, y tenemos a celery para ejecutar las tareas asincronas, crearia un worker que se encargue de enviar esos emails, utilizando alguna libreria de email, y que me los envie asincronicamente para no afectar al flujo de ejecucion.

Me hubiese gustado armar en docker el worker de celery para que se ejecute automaticamente, considero que deberia ser lo ideal.


