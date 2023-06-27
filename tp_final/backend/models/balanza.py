from .recurso import Recurso
from .evento import Evento
from constants import FIN_PESAJE_PLANTA

class Balanza(Recurso):
    def __init__(self, tipo='Balanza', libre=True, camion=None, cola=[]):
        super().__init__(tipo, libre, camion, cola)
        self.tiempo_ocupada = 0

    def pesar_camion(self, reloj, nombre_evento=FIN_PESAJE_PLANTA):
        if len(self.cola) > 0:
            self.libre = False
            self.camion = self.cola.pop(0)
            duracion = self.camion.calcular_tiempo_de_pesaje(reloj)
            self.tiempo_ocupada += duracion - reloj
            return Evento(self.camion, duracion, nombre_evento)
        else:
            self.liberar()