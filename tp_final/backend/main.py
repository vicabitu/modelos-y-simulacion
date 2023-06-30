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
def read_root(anios: int, dias: int, balanzas: int, camiones: int):
    print(f'Anios: {anios}')
    print(f'Dias: {dias}')
    print(f'Camiones: {camiones}')
    return simulacion(anios, dias, balanzas, camiones)