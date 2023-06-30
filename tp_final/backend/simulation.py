import random
import numpy as np
from models.camion import Camion
from models.evento import Evento
from models.planta import Planta
from models.barraca import Barraca
from models.centro_distribucion import CentroDistribucion
from models.centro_reabastecimiento import CentroReabastecimiento
from constants import *

def generar_tipo_de_camion(numero_aleatorio):
    tipo_de_camion = None

    limites = [0.3, 0.55, 0.85, 1]
    tipos = [1, 2, 3, 4]

    for i in range(len(limites)):
        if numero_aleatorio <= limites[i]:
            tipo_de_camion = tipos[i]
            break
    return tipo_de_camion

def generar_camiones(n_camiones):
    camiones = []
    for i in range(n_camiones):
        numero_aleatorio = random.random()
        tipo_de_camion = generar_tipo_de_camion(numero_aleatorio)
        camion = Camion(tipo_de_camion, i)
        camiones.append(camion)
    return camiones

def ordenar_eventos(eventos):
    return sorted(eventos, key=lambda evento: evento.duracion)

def inicializar_eventos(camiones):
    eventos = []
    for camion in camiones:
        duracion = camion.calcular_tiempo_de_viaje(0)
        evento = Evento(camion, duracion, ARRIBO_COLA_CARGA_BARRACA)
        eventos.append(evento)
    return eventos

def resetear_camiones(camiones):
    for c in camiones:
        c.carga_neta = 0

def simulacion(anios: int, dias: int, minutos: int, camiones: int, cant_balanzas: int):
    EXPERIMENTOS = anios
    CORRIDAS = dias
    PUNTO_DE_REORDEN = 8000
    N_CAMIONES = camiones
    mins_simulacion = minutos

    eventos_futuros = []
    barraca = Barraca()
    planta = Planta(mins_simulacion=mins_simulacion, cant_balanzas=cant_balanzas)
    centro_distribucion = CentroDistribucion()
    centro_reabastecimiento = CentroReabastecimiento()
    cantidad_producida_en_cada_anio = [] # Se almacena la produccion total
    promedio_de_produccion_en_cada_anio = []
    camiones = generar_camiones(N_CAMIONES)
    eventos_futuros = ordenar_eventos(inicializar_eventos(camiones))
    for e in eventos_futuros:
        print(e)
    for experimentos in range(EXPERIMENTOS): #años
        print('Comienzo')
        resetear_camiones(camiones)
        reloj = 0
        dia = 1
        cantidad_producida_en_cada_dia = []
        while len(eventos_futuros) > 0 or dia == CORRIDAS:
            nuevos_eventos = []
            nuevo_evento = None
            nuevo_evento_1 = None
            nuevo_evento_2 = None
            evento_actual = eventos_futuros[0]
            print(f'Dia: {int(reloj/ mins_simulacion)} - Cantidad de eventos: {len(eventos_futuros) - 1}')
            reloj = evento_actual.duracion
            print(f'> Reloj: {reloj}')
            print(f"Procesando: {evento_actual}")
            # Barraca:
            if evento_actual.nombre == ARRIBO_COLA_CARGA_BARRACA:
                barraca.encolar_para_carga(evento_actual.objeto)
                if barraca.puede_cargar_camion() and barraca.stock > 0:
                    nuevo_evento = barraca.cargar_camion(reloj)
                    nuevos_eventos.append(nuevo_evento)    
            elif evento_actual.nombre == FIN_CARGA_BARRACA:
                barraca.liberar_puesto_de_carga()
                nuevo_evento_1 = barraca.cargar_camion(reloj)
                camion = evento_actual.objeto
                nuevo_evento_2 = camion.viajar(reloj, materia_prima=True, nombre_evento=ARRIBO_COLA_PESAJE_PLANTA)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])
            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_BARRACA:
                barraca.encolar_para_descarga(evento_actual.objeto)
                if barraca.puede_descargar_camion():
                    nuevo_evento = barraca.descargar_camion(reloj)
                    nuevos_eventos.append(nuevo_evento)
            elif evento_actual.nombre == FIN_DESCARGA_BARRACA:
                barraca.liberar_puesto_de_descarga()
                nuevo_evento_1 = barraca.descargar_camion(reloj)
                camion = evento_actual.objeto
                nuevo_evento_2 = Evento(camion, reloj + 1, ARRIBO_COLA_CARGA_BARRACA)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])
            # Planta:
            elif evento_actual.nombre == ARRIBO_COLA_PESAJE_PLANTA:
                id_balanza = planta.encolar_para_pesaje(evento_actual.objeto)
                if planta.puede_pesar_camion(id_balanza):
                    nuevo_evento = planta.pesar_camion(id_balanza, reloj)
                    nuevos_eventos.append(nuevo_evento) 
            elif evento_actual.nombre == FIN_PESAJE_PLANTA:
                id_balanza = planta.liberar_balanza(evento_actual.objeto)
                nuevo_evento_1 = planta.pesar_camion(id_balanza, reloj)
                camion = evento_actual.objeto
                if camion.materia_prima:
                    nuevo_evento_2 = Evento(camion, reloj + 1, ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA)
                else:
                    nuevo_evento_2 = camion.viajar(reloj, camion.materia_prima, ARRIBO_COLA_DESCARGA_DISTRIBUCION)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])
            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA:
                planta.encolar_para_descarga(evento_actual.objeto)
                if planta.puede_descargar_camion():
                    nuevo_evento = planta.descargar_camion(reloj)
                    nuevos_eventos.append(nuevo_evento)
            elif evento_actual.nombre == FIN_DESCARGA_MATERIA_PRIMA_PLANTA:
                planta.liberar_puesto_de_descarga()
                nuevo_evento_1 = planta.descargar_camion(reloj)
                camion = evento_actual.objeto
                nuevo_evento_2 = Evento(camion, reloj + 1, ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])
                # acá comienza la producción
                eventos_produccion = planta.producir(reloj, dia)
                nuevos_eventos.extend(eventos_produccion)
            elif evento_actual.nombre == FIN_PRODUCCION_PLANTA:
                planta.liberar()
                nuevo_evento = planta.cargar_camion(reloj)
                nuevos_eventos.append(nuevo_evento)
            elif evento_actual.nombre == ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO:
                planta.encolar_para_carga(evento_actual.objeto)
                if planta.puede_cargar_camion():
                    nuevo_evento = planta.cargar_camion(reloj)
                    nuevos_eventos.append(nuevo_evento)
            elif evento_actual.nombre == FIN_CARGA_PRODUCTO_TERMINADO:
                planta.liberar_puesto_de_carga()
                camion = evento_actual.objeto
                camion.materia_prima = False
                nuevo_evento_1 = Evento(camion, reloj + 1, ARRIBO_COLA_PESAJE_PLANTA)
                nuevo_evento_2 = planta.cargar_camion(reloj)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])
            # Centro de distribucion
            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_DISTRIBUCION:
                centro_distribucion.encolar_para_descarga(evento_actual.objeto)
                if centro_distribucion.puede_descargar_camion():
                    nuevo_evento = centro_distribucion.descargar_camion(reloj)
                    nuevos_eventos.append(nuevo_evento)
            elif evento_actual.nombre == FIN_DESCARGA_CAMION_DISTRIBUCION:
                centro_distribucion.liberar_puesto()
                camion = evento_actual.objeto
                nuevo_evento_1 = centro_distribucion.descargar_camion(reloj)
                if barraca.stock <= PUNTO_DE_REORDEN:
                    nuevo_evento_2 = camion.viajar(reloj, materia_prima=False, nombre_evento=ARRIBO_COLA_CARGA_REABASTECIMIENTO)
                else:
                    nuevo_evento_2 = camion.viajar(reloj, materia_prima=False, nombre_evento=ARRIBO_COLA_CARGA_BARRACA)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])
            # Centro reabastecimiento
            elif evento_actual.nombre == ARRIBO_COLA_CARGA_REABASTECIMIENTO:
                centro_reabastecimiento.encolar_para_carga(evento_actual.objeto)
                if centro_reabastecimiento.puede_cargar_camion():
                    nuevo_evento = centro_reabastecimiento.reabastecer_camion(reloj)
                    nuevos_eventos.append(nuevo_evento)
            elif evento_actual.nombre == FIN_CARGA_CAMION_REABASTECIMIENTO:
                centro_reabastecimiento.liberar_puesto()
                camion = evento_actual.objeto
                nuevo_evento_1 = camion.viajar(reloj, materia_prima=True, nombre_evento=ARRIBO_COLA_DESCARGA_BARRACA)
                nuevo_evento_2 = centro_reabastecimiento.reabastecer_camion(reloj)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])
            
            # Elimino los eventos futuros que son None
            nuevos_eventos = [e for e in nuevos_eventos if e is not None]
            eventos_futuros.extend(nuevos_eventos)
            eventos_futuros.remove(evento_actual)
            eventos_futuros = ordenar_eventos(eventos_futuros)

            print(f"Cantidad de stock en la Barraca: {barraca.stock}")

            if int(reloj / mins_simulacion) >= dia: # Fin de un dia
                print(f'Finalice el dia {dia}')
                if dia in planta.produccion_diaria.keys():
                    print(f"Producción diaria: {planta.produccion_diaria[dia] / 1000:.2f} tons")
                dia += 1
            
            if int(reloj / mins_simulacion) >= CORRIDAS:
                # Corto el bucle while de los dias
                break
        
        print('-'*12)
        print('Fin corridas')
        print(f"Corridas completadas: {int(reloj / mins_simulacion)}")
        cantidad_producida_en_cada_dia = [c/1000.0 for c in planta.produccion_diaria.values()]
        print(f'Cantidad producida por cada dia (tons): {cantidad_producida_en_cada_dia}')
        cantidad_producida_en_cada_anio.append(sum(cantidad_producida_en_cada_dia))
        promedio_de_produccion_en_cada_anio.append(np.mean(cantidad_producida_en_cada_dia))
    
    tiempo_total = mins_simulacion * CORRIDAS * EXPERIMENTOS
    tiempos_de_viaje_camiones = [c.tiempo_viajando for c in camiones]
    print(tiempos_de_viaje_camiones)
    print(sum(tiempos_de_viaje_camiones), tiempo_total)
    tiempo_ocupacion_viajando_de_camiones = np.mean(tiempos_de_viaje_camiones) / tiempo_total * 100
    tiempo_sin_viajar_camiones = 100.0 - tiempo_ocupacion_viajando_de_camiones
    print(f'Cantidad producida de todos los anios: {np.sum(cantidad_producida_en_cada_anio)}')
    print(f'Promedio de produccion en cada anio: {promedio_de_produccion_en_cada_anio}')

    print(f"Minutos sin materia prima por dia: \n{planta.tiempos_sin_materia_prima}")

    tiempos_de_ocupacion = planta.tiempos_de_ocupacion_balanzas_pct(tiempo_total)
    print("Array con objs para JSON response:")
    print(f"{tiempos_de_ocupacion=}")

    response = {
        'porcentajesOcupacionBalanzas': tiempos_de_ocupacion,
        'cantidadProducida': f'{cantidad_producida_en_cada_anio[0]}',
        'promedioProduccion': f'{promedio_de_produccion_en_cada_anio[0]}',
        'tiempoPromedioViajandoCamiones': f'{tiempo_ocupacion_viajando_de_camiones}',
        'tiempoPromedioSinViajarCamiones': f'{tiempo_sin_viajar_camiones}',
    }
    return response

if __name__ == "__main__":
    simulacion(1, 10, 900, 15, 3) # 2 balanzas