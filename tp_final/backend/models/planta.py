import math
import numpy as np
from constants import *
from .evento import Evento
from .puesto_de_carga import PuestoCargaDescarga
from .balanza import Balanza

class Planta:
    def __init__(self, mins_simulacion=MINS_SIMULACION, cant_balanzas=1):
        self.libre = True
        self.puesto_de_carga = PuestoCargaDescarga()
        self.puesto_de_descarga = PuestoCargaDescarga()
        self.balanzas = {id_balanza: Balanza(id_=id_balanza) for id_balanza in range(cant_balanzas)}
        self.materia_prima = 0
        self.producto_terminado = 0 # cantidad de producto terminado
        self.producto_terminado_total = 0 # cantidad de producto terminado
        self.produccion_diaria = {}
        self.tiempos_sin_materia_prima = {}
        self.mins_simulacion = mins_simulacion

    def __str__(self):
        estado = 'Libre' if self.libre else 'Ocupada'
        return f'Planta: Libre: {estado}'

    def calcular_tiempo_de_produccion(self, reloj):
        return 10 + round(np.random.exponential(scale=5)) + reloj

    def descontar_tiempo_sin_materia_prima(self, reloj, dia):
        # Asumiendo que la planta tiene cada dia como máximo self.mins_simulacion sin materia prima
        # en este método, se le va descontando a tal valor, los minutos en los que si se dispone
        # de materia prima. 
        # Como resultado se obtiene un diccionario que refleja el tiempo sin materia prima por día.
        # En el día más productivo, el valor es 0 (cero). Caso contrario es self.mins_simulacion sin materia prima.
        
        reloj_actualizado = np.remainder(reloj, self.mins_simulacion) # representa los minutos del dia correspondiente si el reloj se reseteara a 0 todos los dias.
        if not dia in self.tiempos_sin_materia_prima.keys():
            # si el día son 900 min, le restamos el reloj actualizado (que va a oscilar entre 0 y 900)
            self.tiempos_sin_materia_prima.update({dia: int(self.mins_simulacion - reloj_actualizado)})
        else:
            tiempo_restante = self.tiempos_sin_materia_prima[dia]
            if (tiempo_restante - reloj_actualizado) > 0: # para evitar tener valores negativos
                tiempo_restante -= reloj_actualizado
            else:
                self.tiempos_sin_materia_prima[dia] = 0
    
    def producir(self, reloj, dia):
        eventos = []
        if self.materia_prima > CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR and self.libre:
            self.descontar_tiempo_sin_materia_prima(reloj, dia)
            self.libre = False
            ciclos_completos, ciclos_incompletos = self.calcular_ciclos()
            self.materia_prima -= ciclos_completos * 1000 # la cantidad de materia prima es igual a la cantidad de ciclos de producción porque 1.1 ton produce 1 ton
            self.producto_terminado += ciclos_completos * 1000
            self.producto_terminado_total += self.producto_terminado
            inicio = reloj
            
            if dia in self.produccion_diaria.keys():
                self.produccion_diaria[dia] += self.producto_terminado
            else:
                self.produccion_diaria.update({dia: self.producto_terminado})

            for ciclo in range(ciclos_completos):
                duracion = self.calcular_tiempo_de_produccion(inicio)
                evento = Evento(self, duracion, FIN_PRODUCCION_PLANTA)
                duracion_previa = evento.duracion
                eventos.append(evento)
                if ciclo > 0:
                    inicio += duracion_previa
        return eventos

    def liberar(self):
        self.libre = True

    def calcular_ciclos(self):
        # Opc. 1: entran 7 ton -> se producen 7 ton
        # Opc. 2: entran 7 ton -> hacer regla de 3. sabiendo que por cada 1.1 ton materia prima sale 1 ton de prod. terminado
        # ejemplo: aca producimos 0.5 toneladas por cada 1.1 ton de materia prima
        # 1.1 --> 0.5
        # 7 --> x
        # (7 * 0.5) / 1.1 -> 3.5 / 1.1 = 3.18 ton prod terminado
        #  7 / 1.1 = 7 - 6.3 = 0.7 # sobran 0.7 ton materia prima
        ciclos = self.materia_prima / CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR
        ciclo_incompleto, ciclos_completos = math.modf(ciclos) # ciclo_incompleto da un número con coma.
        return int(ciclos_completos), round(ciclo_incompleto, 3)


    def cargar_camion(self, reloj, nombre_evento=FIN_CARGA_PRODUCTO_TERMINADO):
        # carga el camion con producto terminado
        if self.producto_terminado > 0:
            evento = self.puesto_de_carga.cargar_camion(reloj, nombre_evento)
            # Aca le doy el producto que puedo, todo o una parte
            if evento:
                if evento.objeto.carga_neta > self.producto_terminado:
                    evento.objeto.carga_neta = self.producto_terminado
                self.producto_terminado -= evento.objeto.carga_neta
            return evento

    def descargar_camion(self, reloj, nombre_evento=FIN_DESCARGA_MATERIA_PRIMA_PLANTA):
        # carga el camion con materia prima
        evento, carga = self.puesto_de_descarga.descargar_camion(reloj, nombre_evento)
        if evento:
            self.materia_prima += carga
        return evento

    def pesar_camion(self, id_balanza, reloj):
        return self.balanzas[id_balanza].pesar_camion(reloj, FIN_PESAJE_PLANTA)

    def encolar_para_descarga(self, camion):
        self.puesto_de_descarga.cola.append(camion)

    def encolar_para_carga(self, camion):
        self.puesto_de_carga.cola.append(camion)

    def encolar_para_pesaje(self, camion):
        # elegimos una balanza de manera aleatoria
        idx_balanza = np.random.randint(0, len(self.balanzas))
        balanza = self.balanzas[idx_balanza]
        balanza.cola.append(camion)
        return balanza.id

    def liberar_puesto_de_carga(self):
        self.puesto_de_carga.liberar()

    def liberar_puesto_de_descarga(self):
        self.puesto_de_descarga.liberar()

    def liberar_balanza(self, camion):
        # buscamos y liberamos aquella balanza que tiene asociado al camion que viene por parámetros
        for balanza in self.balanzas.values():
            if balanza.camion == camion:
                balanza.liberar()
                return balanza.id

    def puede_pesar_camion(self, id_balanza):
        return self.balanzas[id_balanza].libre

    def puede_descargar_camion(self):
        return self.puesto_de_descarga.libre

    def puede_cargar_camion(self):
        return self.puesto_de_carga.libre

    def produccion_total_en_tons(self):
        return self.producto_terminado_total / 1000

    def tiempos_de_ocupacion_balanzas(self):
        return {balanza.id: balanza.tiempo_ocupada for balanza in self.balanzas}

    def tiempos_de_ocupacion_balanzas_pct(self, tiempo_total):
        tiempos_de_ocupacion = []
        for id_, balanza in self.balanzas.items():
            ocupacion_en_pct = balanza.tiempo_ocupada / tiempo_total * 100
            tiempos_de_ocupacion.append({
                "id": id_ + 1,
                "ocupacion": f'{ocupacion_en_pct:.2f}', 
                "ociosos": f'{100.0 - ocupacion_en_pct:.2f}'
            })
        return tiempos_de_ocupacion
    
    def calcular_promedio_de_tiempo_sin_materia_prima(self):
        tiempos = [tiempo for tiempo in self.tiempos_sin_materia_prima.values()]
        return np.mean(tiempos)