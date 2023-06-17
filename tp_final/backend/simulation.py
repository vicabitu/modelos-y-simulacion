import random
import numpy as np

from models.camion import Camion
from models.evento import Evento
from models.recurso import Recurso
from constants import (
    TIEMPOS_DE_VIAJE,
    PESAJES_CAMIONES,
    TIEMPOS_CARGA_DESCARGA,
    CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR
)

# Eventos Barraca:
ARRIBO_COLA_CARGA_BARRACA = 'ACCB'
FIN_CARGA_BARRACA = 'FCB'
ARRIBO_COLA_DESCARGA_BARRACA = 'ACDB'
FIN_DESCARGA_BARRACA = 'FDB'
SOLICITUD_MATERIA_PRIMA_BARRACA = 'SMPB'
# Eventos Planta:
ARRIBO_COLA_PESAJE_PLANTA = 'ACPP'
FIN_PESAJE_PLANTA = 'FPP'

ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA = 'ACDMPP'
FIN_DESCARGA_MATERIA_PRIMA_PLANTA = 'FDMPP'

ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO = 'ACCPT'
FIN_CARGA_PRODUCTO_TERMINADO = 'FCPP'

FIN_PESAJE_PRODUCTO_TERMINADO = 'FPPT' # este evento es el que activa al camion a que vaya al centro de distribucion

FIN_PRODUCCION_PLANTA = 'FPP'
# Centro de distribucion
ARRIBO_COLA_DESCARGA_DISTRIBUCION = 'ACDD'
FIN_DESCARGA_CAMION_DISTRIBUCION = 'FDCD'
# Centro reabastecimiento
ARRIBO_COLA_CARGA_REABASTECIMIENTO = 'ACCR'
FIN_CARGA_CAMION_REABASTECIMIENTO = 'FCCR'

def generar_tipo_de_camion(numero_aleatorio):
    tipo_de_camion = None

    limites = [0.3, 0.55, 0.85, 1]
    tipos = [1, 2, 3, 4]

    for i in range(len(limites)):
        if numero_aleatorio <= limites[i]:
            tipo_de_camion = tipos[i]
            break
    return tipo_de_camion

def generar_camiones():
    camiones = []
    for i in range(15):
        numero_aleatorio = random.random()
        tipo_de_camion = generar_tipo_de_camion(numero_aleatorio)
        camion = Camion(tipo_de_camion)
        camiones.append(camion)
    return camiones

def calcular_tiempo_de_viaje_segun_tipo_de_camion(tipo_de_camion):
    media = TIEMPOS_DE_VIAJE.get(tipo_de_camion).get('media')
    desvio = TIEMPOS_DE_VIAJE.get(tipo_de_camion).get('desvio')
    # print(f'Media: {media} - Desvio: {desvio}')
    return round(np.random.normal(loc=media, scale=desvio))

def calcular_pesaje_segun_tipo_de_camion(tipo_de_camion):
    media = PESAJES_CAMIONES.get(tipo_de_camion).get('media')
    desvio = PESAJES_CAMIONES.get(tipo_de_camion).get('desvio')
    # print(f'Media: {media} - Desvio: {desvio}')
    return round(np.random.normal(loc=media, scale=desvio))

def calcular_tiempo_de_produccion_de_planta():
    return 10 + round(np.random.exponential(scale=5))

def obtener_tiempo_carga_descarga_segun_tipo_de_camion(tipo_de_camion):
    return TIEMPOS_CARGA_DESCARGA.get(tipo_de_camion)

def ordenar_eventos(eventos):
    return sorted(eventos, key=lambda evento: evento.duracion)

def calcular_tiempo_de_pesaje_segun_tipo_de_camion(tipo_de_camion):
    return 11

def inicializar_eventos(camiones):
    eventos = []
    for camion in camiones:
        duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(camion.tipo)
        # print(f'Tiempo de viaje: {duracion}')
        evento = Evento(camion, duracion, ARRIBO_COLA_CARGA_BARRACA)
        eventos.append(evento)
    return eventos

def simulacion():
    EXPERIMENTOS = 1
    CORRIDAS = 1
    PUNTO_DE_REORDEN = 8000

    cantidad_materia_prima_en_planta = 0
    stock_en_barraca = 20000
    reloj = 0
    eventos_futuros = []
    cantidad_de_producto_terminada_en_planta = 0
    puesto_de_carga_barraca = Recurso()
    puesto_de_descarga_barraca = Recurso()
    puesto_de_descarga_planta = Recurso()
    puesto_de_carga_planta = Recurso()
    puesto_de_carga_centro_distribucion = Recurso()
    puesto_de_descarga_centro_distribucion = Recurso()
    puesto_de_carga_centro_reabastecimiento = Recurso()
    puesto_de_descarga_centro_reabastecimiento = Recurso()

    cantidad_de_produccion_diaria = 0

    balanza_planta = Recurso('Balanza')

    print('Simulacion')
    camiones = generar_camiones()
    for camion in camiones:
        print(f'{camion} - valor pesaje: {calcular_pesaje_segun_tipo_de_camion(camion.tipo)}')
    eventos_futuros = ordenar_eventos(inicializar_eventos(camiones))
    for evento in eventos_futuros:
        print(evento)
    for experimentos in range(EXPERIMENTOS): #años
        for corridas in range(CORRIDAS): #dias
            print('Comienzo')
            while reloj <= 900:
                nuevo_evento = None
                evento_actual = eventos_futuros[0]
                # Barraca:
                if evento_actual.nombre == ARRIBO_COLA_CARGA_BARRACA:
                    # Aca directamente pasa de una, no se tiene en cuenta el arribo al puesto de carga.
                    print(f'Evento: {ARRIBO_COLA_CARGA_BARRACA}')
                    reloj += evento_actual.duracion
                    if puesto_de_carga_barraca.libre:

                        # Esto se hace siempre en el arribo de...
                        puesto_de_carga_barraca.cola.append(nuevo_evento.objeto)
                        camion = puesto_de_carga_barraca.cola.pop(0) # es el primero de la cola y lo saco

                        puesto_de_carga_barraca.camion = camion
                        puesto_de_carga_barraca.libre = False
                        duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion) + reloj
                        nuevo_evento = Evento(camion, duracion, FIN_CARGA_BARRACA)
                        camion.set_carga()
                    else:
                        puesto_de_carga_barraca.cola.append(evento_actual.objeto)
                elif evento_actual.nombre == FIN_CARGA_BARRACA:
                    print(f'Evento: {FIN_CARGA_BARRACA}')
                    reloj += evento_actual.duracion
                    # puesto_de_carga_barraca.eliminar_camion(evento_actual.objeto) # Porque elimino el camion?
                    puesto_de_descarga_planta.libre = True
                    stock_en_barraca -= evento_actual.objeto.carga_neta
                    duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                    nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_PESAJE_PLANTA)
                elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_BARRACA:
                    print(f'Evento: {ARRIBO_COLA_DESCARGA_BARRACA}')
                    reloj += evento_actual.duracion
                    if puesto_de_descarga_barraca.libre:
                        puesto_de_descarga_barraca.cola.append(nuevo_evento.objeto)
                        camion = puesto_de_descarga_barraca.cola.pop(0)
                        puesto_de_descarga_barraca.camion = camion
                        puesto_de_descarga_barraca.libre = False
                        duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion) + reloj
                        nuevo_evento = Evento(camion, duracion, FIN_DESCARGA_BARRACA)
                    else:
                        puesto_de_descarga_barraca.cola.append(evento_actual.objeto)
                elif evento_actual.nombre == FIN_DESCARGA_BARRACA:
                    print(f'Evento: {FIN_DESCARGA_BARRACA}')
                    reloj += evento_actual.duracion
                    stock_en_barraca += evento_actual.objeto.carga_neta
                    evento_actual.objeto.carga_neta = 0
                    nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_CARGA_BARRACA)
                    puesto_de_descarga_barraca.libre = True
                # Planta:
                elif evento_actual.nombre == ARRIBO_COLA_PESAJE_PLANTA:
                    print(f'Evento: {ARRIBO_COLA_PESAJE_PLANTA}')
                    reloj += evento_actual.duracion
                    if balanza_planta.libre:
                        balanza_planta.cola.append(nuevo_evento.objeto)
                        camion = balanza_planta.cola.pop(0)
                        balanza_planta.camion = camion
                        balanza_planta.libre = False
                        duracion = calcular_tiempo_de_pesaje_segun_tipo_de_camion(camion)
                        # balanza_planta.eliminar_camion(evento_actual.objeto)
                        nuevo_evento = Evento(camion, duracion, FIN_PESAJE_PLANTA)
                    else:
                        balanza_planta.cola.append(evento_actual.objeto)
                elif evento_actual.nombre == FIN_PESAJE_PLANTA:
                    print(f'Evento: {FIN_PESAJE_PLANTA}')
                    reloj += evento_actual.duracion
                    balanza_planta.libre = True
                    if evento_actual.objeto.materia_prima:
                        nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA)
                    else: 
                        duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo) + reloj
                        nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_DESCARGA_DISTRIBUCION)
                elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA:
                    print(f'Evento: {ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA}')
                    reloj += evento_actual.duracion
                    if puesto_de_descarga_planta.libre:
                        puesto_de_descarga_planta.cola.append(nuevo_evento.objeto)
                        camion = puesto_de_descarga_planta.cola.pop(0)
                        puesto_de_descarga_planta.camion = camion
                        puesto_de_carga_planta.libre = False
                        duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(evento_actual.objeto.tipo)
                        nuevo_evento = Evento(evento_actual.objeto, duracion, FIN_DESCARGA_MATERIA_PRIMA_PLANTA)
                    else:
                        puesto_de_descarga_planta.cola.append(evento_actual.objeto)
                elif evento_actual.nombre == FIN_DESCARGA_MATERIA_PRIMA_PLANTA:
                    reloj += evento_actual.duracion
                    cantidad_materia_prima_en_planta += evento_actual.objeto.carga_neta
                    evento_actual.objeto.carga_neta = 0
                    nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO)
                    puesto_de_descarga_planta.libre = True
                    if cantidad_materia_prima_en_planta >= CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR: #Empiezo a producir
                        duracion = calcular_tiempo_de_produccion_de_planta()
                        nuevo_evento = Evento('Aca no se que va', duracion, FIN_PRODUCCION_PLANTA)
                        # Aca debo agregar el evento en la lista, como en todos lados en donde se instancia.
                    
                elif evento_actual.nombre == ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO:
                    print(f'Evento: {ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO}')
                    # Aca deberia preguntar si hay producto terminado?
                    reloj += evento_actual.duracion
                    if cantidad_de_producto_terminada_en_planta > 0:
                        if puesto_de_carga_planta.libre:
                            puesto_de_carga_planta.cola.append(nuevo_evento.objeto)
                            camion = puesto_de_carga_planta.cola.pop(0)
                            puesto_de_carga_planta.camion = camion
                            camion.set_carga()
                            duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion) + reloj
                            nuevo_evento = Evento(camion, duracion, FIN_CARGA_PRODUCTO_TERMINADO)
                            # aca al evento lo tengo que agregar a la lista de eventos futuros
                        else:
                            puesto_de_carga_planta.cola.append(nuevo_evento.objeto)
                elif evento_actual.nombre == FIN_CARGA_PRODUCTO_TERMINADO:
                    reloj += evento_actual.duracion
                    nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_PESAJE_PLANTA)
                    puesto_de_carga_planta.libre = True
                    cantidad_de_producto_terminada_en_planta -= nuevo_evento.objeto.carga_neta
                    # aca al evento lo tengo que agregar a la lista de eventos futuros
                elif evento_actual.nombre == FIN_PRODUCCION_PLANTA:
                    print(f'Evento: {FIN_PRODUCCION_PLANTA}')
                    cantidad_de_producto_terminada_en_planta += 10000
                    # Aca tengo que tomar un camion de la cola de carga de producto terminado?
                # Centro de distribucion
                elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_DISTRIBUCION:
                    print(f'Evento: {ARRIBO_COLA_DESCARGA_DISTRIBUCION}')
                    # Puesto de descarga libre o ocupado
                    reloj += evento_actual.duracion
                    if puesto_de_descarga_centro_distribucion.libre:
                        cantidad_de_produccion_diaria += evento_actual.objeto.carga # calcula para las estadisticas
                        puesto_de_descarga_centro_reabastecimiento.cola.append(nuevo_evento.objeto)
                        camion = puesto_de_descarga_centro_reabastecimiento.cola.pop(0)
                        puesto_de_descarga_centro_reabastecimiento.camion = camion
                        camion.carga_neta = 0
                        duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion)
                        nuevo_evento = Evento(camion, duracion, FIN_DESCARGA_CAMION_DISTRIBUCION)
                    else:
                        puesto_de_descarga_centro_distribucion.cola.append(evento_actual.objeto)
                elif evento_actual.nombre == FIN_DESCARGA_CAMION_DISTRIBUCION: # en que momento calculo el tiempo que va a tardar en descargar
                    reloj += evento_actual.duracion
                    if stock_en_barraca <= PUNTO_DE_REORDEN:
                        duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                        nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_CARGA_REABASTECIMIENTO)
                    else:
                        duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                        nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_CARGA_BARRACA)
                    puesto_de_descarga_centro_distribucion.libre = True
                # Centro reabastecimiento
                elif evento_actual.nombre == ARRIBO_COLA_CARGA_REABASTECIMIENTO:
                    print(f'Evento: {ARRIBO_COLA_CARGA_REABASTECIMIENTO}')
                    reloj += evento_actual.duracion
                    if puesto_de_carga_centro_reabastecimiento.libre:
                        puesto_de_carga_centro_reabastecimiento.cola.append(nuevo_evento.objeto)
                        camion = puesto_de_carga_centro_reabastecimiento.cola.pop(0)
                        puesto_de_carga_centro_reabastecimiento.camion = camion
                        camion.set_carga(10) # Aca lo tengo que cargar al maximo, hacer un metodo en la clase camion, el metodo que hay ahora no va mas
                        duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion)
                        nuevo_evento = Evento(camion, duracion, FIN_CARGA_CAMION_REABASTECIMIENTO)
                    else:
                        puesto_de_carga_centro_reabastecimiento.cola.append(evento_actual.objeto)
                elif evento_actual.nombre == FIN_CARGA_CAMION_REABASTECIMIENTO:
                    reloj += evento_actual.duracion
                    duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                    nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_DESCARGA_BARRACA)
                
                if not nuevo_evento is None:
                    eventos_futuros.append(nuevo_evento)
                    eventos_futuros = ordenar_eventos(eventos_futuros)

                # Eliminar el evento atendido

if __name__ == '__main__':
    simulacion()
