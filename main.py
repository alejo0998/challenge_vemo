# docker run --name postgres -e POSTGRES_PASSWORD=password -p 5433:5433 -d postgres
from fastapi import FastAPI
from paises.views import router as paises_router

app = FastAPI()
app.include_router(paises_router)



@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
