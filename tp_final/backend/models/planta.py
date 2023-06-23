from constants import *

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