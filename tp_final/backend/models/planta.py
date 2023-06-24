import math
import numpy as np
from constants import *
from .evento import Evento

class Planta:
    def __init__(self):
        self.libre = True

    def __str__(self):
        estado = 'Libre' if self.libre else 'Ocupada'
        return f'Planta: Libre: {estado}'

    def calcular_tiempo_de_produccion(self, reloj):
        return 10 + round(np.random.exponential(scale=5)) + reloj

    def producir(self, reloj):
        self.libre = False
        duracion = self.calcular_tiempo_de_produccion(reloj)
        return Evento(self, duracion, FIN_PRODUCCION_PLANTA)

    def liberar(self):
        self.libre = True

    def calcular_ciclos(self, cantidad_materia_prima_en_planta):
        # Opc. 1: entran 7 ton -> se producen 7 ton
        # Opc. 2: entran 7 ton -> hacer regla de 3. sabiendo que por cada 1.1 ton materia prima sale 1 ton de prod. terminado
        # ejemplo: aca producimos 0.5 toneladas por cada 1.1 ton de materia prima
        # 1.1 --> 0.5
        # 7 --> x
        # (7 * 0.5) / 1.1 -> 3.5 / 1.1 = 3.18 ton prod terminado
        #  7 / 1.1 = 7 - 6.3 = 0.7 # sobran 0.7 ton materia prima
        ciclos = cantidad_materia_prima_en_planta / CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR
        ciclo_incompleto, ciclos_completos = math.modf(ciclos) # ciclo_incompleto da un número con coma.
        return int(ciclos_completos), round(ciclo_incompleto, 3)
