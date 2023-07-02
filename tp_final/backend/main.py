from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from simulation import simulacion

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def read_root(anios: int, dias: int, minutos: int, camiones: int, cant_balanzas: int):
    print(f'Anios: {anios}')
    print(f'Dias: {dias}')
    print(f'Minutos: {minutos}')
    print(f'Camiones: {camiones}')
    print(f'Balanzas: {cant_balanzas}')
    return simulacion(anios, dias, minutos, camiones, cant_balanzas)