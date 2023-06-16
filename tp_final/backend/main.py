from fastapi import FastAPI

from simulation import simulacion

app = FastAPI()

@app.get("/")
def read_root():
    simulacion()
    return {"Hello": "World"}