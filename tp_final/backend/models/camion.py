import numpy as np
from constants import (
    PESO_CAMIONES, PESAJES_CAMIONES
)

class Camion:
    def __init__(self, tipo, id, materia_prima=True):
        self.tipo = tipo
        self.materia_prima = materia_prima #materia prima o producto terminado
        self.carga_neta = 0
        self.id = id
    
    def set_carga(self):
        pesaje = self.calcular_pesaje_segun_tipo_de_camion()
        if pesaje < PESO_CAMIONES.get(self.tipo).get('sin_carga'):
            pesaje = PESO_CAMIONES.get(self.tipo).get('sin_carga')
        elif pesaje > PESO_CAMIONES.get(self.tipo).get('peso_maximo'):
            pesaje = PESO_CAMIONES.get(self.tipo).get('peso_maximo')
        self.carga_neta = pesaje - PESO_CAMIONES.get(self.tipo).get('sin_carga')

    def calcular_pesaje_segun_tipo_de_camion(self):
        media = PESAJES_CAMIONES.get(self.tipo).get('media')
        desvio = PESAJES_CAMIONES.get(self.tipo).get('desvio')
        return round(np.random.normal(loc=media, scale=desvio))
    
    def cargar_al_maximo(self):
        peso_minimo = PESO_CAMIONES.get(self.tipo)['sin_carga']
        peso_maximo = PESO_CAMIONES.get(self.tipo)['peso_maximo']
        self.carga_neta = peso_maximo - peso_minimo
    
    def __str__(self):
        return f'ID: {self.id} - Tipo: {self.tipo} - Carga: {self.carga_neta}'
