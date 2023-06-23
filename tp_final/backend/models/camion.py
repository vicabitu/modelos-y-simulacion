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

    def calcular_tiempo_de_viaje(self, reloj):
        media = TIEMPOS_DE_VIAJE.get(self.tipo).get('media')
        desvio = TIEMPOS_DE_VIAJE.get(self.tipo).get('desvio')
        return round(np.random.normal(loc=media, scale=desvio)) + reloj

    def calcular_tiempo_carga_descarga(self, reloj):
        #print(f'Tiempo de carga/descarga: {TIEMPOS_CARGA_DESCARGA.get(tipo_de_camion)}')
        return TIEMPOS_CARGA_DESCARGA.get(self.tipo) + reloj

    def calcular_tiempo_de_pesaje(self, reloj): 
        return round(np.random.normal(loc=11, scale=3)) + reloj

    def calcular_pesaje(self):
        media = PESAJES_CAMIONES.get(self.tipo).get('media')
        desvio = PESAJES_CAMIONES.get(self.tipo).get('desvio')
        return round(np.random.normal(loc=media, scale=desvio))

    def viajar(self, reloj, materia_prima=False, nombre_evento=ARRIBO_COLA_CARGA_BARRACA):
        duracion = self.calcular_tiempo_de_viaje(reloj)
        self.materia_prima = materia_prima # que transporta el camion? si es materia prima entonces True, sino False
        return Evento(self, duracion, nombre_evento)
    
    def descargar(self, reloj):
        self.vaciar()
        duracion = self.calcular_tiempo_carga_descarga(reloj)
        return duracion

    def cargar(self, reloj, peso):
        self.carga_neta = peso
        duracion = self.calcular_tiempo_carga_descarga(reloj)
        return duracion

    def cargar_al_maximo(self, reloj):
        peso_minimo = PESO_CAMIONES.get(self.tipo)['sin_carga']
        peso_maximo = PESO_CAMIONES.get(self.tipo)['peso_maximo']
        self.carga_neta = peso_maximo - peso_minimo
        duracion = self.calcular_tiempo_carga_descarga(reloj)
        return duracion


    def vaciar(self):
        self.carga_neta = 0
    
    def __str__(self):
        return f'Camión: {self.id} - Tipo: {self.tipo} - Carga: {self.carga_neta}'