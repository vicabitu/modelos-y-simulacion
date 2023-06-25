from .recurso import Recurso
from .evento import Evento
from constants import *

class PuestoCargaDescarga(Recurso):

    def cargar_camion(self, reloj, nombre_evento=FIN_CARGA_BARRACA):
        if len(self.cola) > 0:
            self.camion = self.cola.pop(0)
            self.libre = False
            self.camion.set_carga()
            duracion = self.camion.calcular_tiempo_carga_descarga(reloj)
            return Evento(self.camion, duracion, nombre_evento)
        else:
            self.liberar()

    def cargar_con_peso_especifico(self, reloj, peso, nombre_evento=FIN_CARGA_PRODUCTO_TERMINADO):
        if len(self.cola) > 0:
            self.camion = self.cola.pop(0)
            self.libre = False
            duracion = self.camion.cargar(peso)
            return Evento(self.camion, duracion, nombre_evento)
        else:
            self.liberar()

    def descargar_camion(self, reloj, nombre_evento=FIN_DESCARGA_BARRACA):
        if len(self.cola) > 0:
            self.camion = self.cola.pop(0)
            self.libre = False
            duracion = self.camion.descargar(reloj)
            return Evento(self.camion, duracion, nombre_evento)
        else:
            self.liberar()

    def reabastecer_camion(self, reloj):
        if len(self.cola) > 0:
            self.camion = self.cola.pop(0)
            self.libre = False
            duracion = self.camion.cargar_al_maximo(reloj)
            return Evento(self.camion, duracion, FIN_CARGA_CAMION_REABASTECIMIENTO)
        else:
            self.liberar()
