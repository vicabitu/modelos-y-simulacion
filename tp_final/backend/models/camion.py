import numpy as np
from constants import (
    PESO_CAMIONES, PESAJES_CAMIONES
)

class Camion:
    def __init__(self, tipo, materia_prima=True):
        self.tipo = tipo
        self.materia_prima = materia_prima #materia prima o producto terminado
        self.carga_neta = 0
    
    def set_carga(self):
        pesaje = self.calcular_pesaje_segun_tipo_de_camion()
        if pesaje < PESO_CAMIONES.get(self.tipo)['sin_carga']:
            pesaje = PESO_CAMIONES.get(self.tipo)['sin_carga']
        elif pesaje > PESO_CAMIONES.get(self.tipo)['peso_maximo']:
            pesaje = PESO_CAMIONES.get(self.tipo)['peso_maximo']
        self.carga_neta = pesaje - PESO_CAMIONES.get(self.tipo)['sin_carga']

    def calcular_pesaje_segun_tipo_de_camion(self):
        media = PESAJES_CAMIONES.get(self.tipo).get('media')
        desvio = PESAJES_CAMIONES.get(self.tipo).get('desvio')
        return round(np.random.normal(loc=media, scale=desvio))
    
    def __str__(self):
        return f'Tipo: {self.tipo} - Carga: {self.carga_neta}'
