from fastapi import FastAPI
from routers import metrics, rutaTerrestre , vecindad, avancedSearch

app = FastAPI()


app.include_router(vecindad.router)
app.include_router(metrics.router)
app.include_router(rutaTerrestre.router)
app.include_router(avancedSearch.router)

@app.get("/")
def hola():
    return {"mensaje" : "hola"}

@app.get("/saludo/{nombre}")
def saludar(nombre : str):
    return {"saludo": f"hola {nombre}, bienvenido a fast api"}