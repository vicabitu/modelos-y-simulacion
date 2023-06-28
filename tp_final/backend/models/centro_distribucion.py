from constants import *
from .puesto_de_carga import PuestoCargaDescarga

class CentroDistribucion():
    def __init__(self):
        self.puesto_de_descarga = PuestoCargaDescarga()
        self.producto_distribuido_total = 0

    def descargar_camion(self, reloj):
        evento, carga = self.puesto_de_descarga.descargar_camion(reloj, FIN_DESCARGA_CAMION_DISTRIBUCION)
        if evento:
            self.producto_distribuido_total += carga
        return evento
 
    def puede_descargar_camion(self):
        return self.puesto_de_descarga.libre

    def encolar_para_descarga(self, camion):
        self.puesto_de_descarga.cola.append(camion)

    def liberar_puesto(self):
        self.puesto_de_descarga.liberar()