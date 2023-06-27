from constants import *
from .puesto_de_carga import PuestoCargaDescarga

class Barraca():
    def __init__(self):
        self.puesto_de_carga = PuestoCargaDescarga()
        self.puesto_de_descarga = PuestoCargaDescarga()
        self.stock = STOCK_EN_BARRACA
    
    def stock_alcanza(self, carga):
        return self.stock >= carga

    def cargar_camion(self, reloj, nombre_evento=FIN_CARGA_BARRACA):
        evento = self.puesto_de_carga.cargar_camion(reloj, nombre_evento)

        if evento:
            if self.stock_alcanza(evento.objeto.carga_neta):
                self.stock -= evento.objeto.carga_neta
            else:
                evento.objeto.carga_neta = self.stock
                self.stock = 0
        return evento

    def descargar_camion(self, reloj, nombre_evento=FIN_DESCARGA_BARRACA):
        evento, carga = self.puesto_de_descarga.descargar_camion(reloj, nombre_evento)
        if evento:
            self.stock += carga
        return evento

    def encolar_para_descarga(self, camion):
        self.puesto_de_descarga.cola.append(camion)

    def encolar_para_carga(self, camion):
        self.puesto_de_carga.cola.append(camion)

    def liberar_puesto_de_carga(self):
        self.puesto_de_carga.liberar()

    def liberar_puesto_de_descarga(self):
        self.puesto_de_descarga.liberar()

    def puede_descargar_camion(self):
        return self.puesto_de_descarga.libre

    def puede_cargar_camion(self):
        return self.puesto_de_carga.libre