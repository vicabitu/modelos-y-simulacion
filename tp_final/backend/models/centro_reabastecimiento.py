from constants import *
from .puesto_de_carga import PuestoCargaDescarga

class CentroReabastecimiento():
    def __init__(self):
        self.puesto_de_carga = PuestoCargaDescarga()
        self.producto_reabastecido_total = 0

    def reabastecer_camion(self, reloj):
        evento = self.puesto_de_carga.reabastecer_camion(reloj)
        if evento:
            self.producto_reabastecido_total += evento.objeto.carga_neta
        return evento

    # def cargar_camion(self, reloj):
    #     evento = self.puesto_de_carga.cargar_camion(reloj, FIN_CARGA_CAMION_REABASTECIMIENTO)
    #     if evento:
    #         self.producto_reabastecido_total += evento.objeto.carga_neta
    #     return evento
 
    def puede_cargar_camion(self):
        return self.puesto_de_carga.libre

    def encolar_para_carga(self, camion):
        self.puesto_de_carga.cola.append(camion)

    def liberar_puesto(self):
        self.puesto_de_carga.liberar()