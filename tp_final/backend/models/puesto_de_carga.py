from .recurso import Recurso
from constants import *

class PuestoCargaDescarga(Recurso):
    def __init__(self, tipo='Puesto', libre=True, camion=None, cola=[]):
        super().__init__(tipo, libre, camion, cola)

    def cargar_camion(self, reloj, nombre_evento=FIN_CARGA_BARRACA):
        if len(self.cola) > 0:
            camion = self.cola.pop(0)
            self.camion = camion
            self.libre = False
            camion.set_carga()
            duracion = camion.calcular_tiempo_carga_descarga(reloj)
            return Evento(camion, duracion, nombre_evento)
        else:
            self.liberar()

    def cargar_con_peso_especifico(self, reloj, peso, nombre_evento=FIN_CARGA_PRODUCTO_TERMINADO):
        if len(self.cola) > 0:
            camion = self.cola.pop(0)
            self.camion = camion
            self.libre = False
            duracion = camion.cargar(peso)
            return Evento(camion, duracion, nombre_evento)
        else:
            self.liberar()

    def descargar_camion(self, reloj, nombre_evento=FIN_DESCARGA_BARRACA):
        if len(self.cola) > 0:
            camion = self.cola.pop(0)
            self.libre = False
            self.camion = camion
            duracion = self.camion.descargar(reloj)
            return Evento(self.camion, duracion, nombre_evento)
        else:
            self.liberar()

    def reabastecer_camion(self, reloj):
        duracion = self.camion.cargar_al_maximo(reloj)
        return Evento(self.camion, duracion, FIN_CARGA_CAMION_REABASTECIMIENTO)

