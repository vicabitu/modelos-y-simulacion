import random
import numpy as np

from models.camion import Camion
from models.evento import Evento
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
FIN_PESAJE_MATERIA_PRIMA_PLANTA = 'FPMPP'

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
                if evento_actual.nombre == ARRIBO_COLA_CARGA_BARRACA: # Este evento lo tengo que atender?
                    # Aca en tal caso tendria que generar un evento para saber cuando arribaria al puesto de carga de materia prima?
                    print(f'Evento: {ARRIBO_COLA_CARGA_BARRACA}')
                elif evento_actual.nombre == FIN_CARGA_BARRACA:
                    print(f'Evento: {FIN_CARGA_BARRACA}')
                    duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                    nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_PESAJE_PLANTA)
                    # Descuento en la barraca el valor de pesaje del camion
                    stock_en_barraca -= evento_actual.objeto.carga
                    reloj += evento_actual.duracion
                elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_BARRACA:
                    print(f'Evento: {ARRIBO_COLA_DESCARGA_BARRACA}')
                elif evento_actual.nombre == FIN_DESCARGA_BARRACA:
                    print(f'Evento: {FIN_DESCARGA_BARRACA}')
                    stock_en_barraca += evento_actual.objeto.carga
                    evento_actual.objeto.carga.set_carga(0)
                    nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_CARGA_BARRACA)
                    # Aca cuanto avanzo el reloj?
                elif evento_actual.nombre == SOLICITUD_MATERIA_PRIMA_BARRACA:
                    print(f'Evento: {SOLICITUD_MATERIA_PRIMA_BARRACA}')
                
                elif evento_actual.nombre == ARRIBO_COLA_PESAJE_PLANTA:
                    print(f'Evento: {ARRIBO_COLA_PESAJE_PLANTA}')
                elif evento_actual.nombre == FIN_PESAJE_MATERIA_PRIMA_PLANTA:
                    print(f'Evento: {FIN_PESAJE_MATERIA_PRIMA_PLANTA}')
                    nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA)
                    # Aca cuanto avanzo el reloj?
                elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA:
                    print(f'Evento: {ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA}')
                elif evento_actual.nombre == FIN_DESCARGA_MATERIA_PRIMA_PLANTA:
                    cantidad_materia_prima_en_planta += evento_actual.objeto.carga
                    if cantidad_materia_prima_en_planta >= CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR: #Empiezo a producir
                        duracion = calcular_tiempo_de_produccion_de_planta()
                        nuevo_evento = Evento('Aca no se que va', duracion, FIN_PRODUCCION_PLANTA)
                        reloj += evento_actual.duracion
                    else:
                        nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO)
                        # Aca cuanto avanzo el reloj?
                    evento_actual.objeto.carga.set_carga(0)
                elif evento_actual.nombre == ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO:
                    print(f'Evento: {ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO}')
                elif evento_actual.nombre == FIN_CARGA_PRODUCTO_TERMINADO: # En que momento genero este evento?
                    nuevo_evento = Evento(evento_actual.objeto, 'duracion?', 'ARRIBO_COLA_PESAJE_PLANTA?')
                elif evento_actual.nombre == 'ARRIBO_COLA_PESAJE_PRODUCTO_TERMINADO?': # aca no se que va porque se entiendo que hay una sola cola de pesaje y una sola balanza.
                    print('ARRIBO_COLA_PESAJE_PRODUCTO_TERMINADO?')
                elif evento_actual.nombre == FIN_PESAJE_PRODUCTO_TERMINADO:
                    duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                    nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_DESCARGA_DISTRIBUCION)
                    reloj += evento_actual.duracion
                elif evento_actual.nombre == FIN_PRODUCCION_PLANTA:
                    print(f'Evento: {FIN_PRODUCCION_PLANTA}')
                
                elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_DISTRIBUCION:
                    print(f'Evento: {ARRIBO_COLA_DESCARGA_DISTRIBUCION}')
                elif evento_actual.nombre == FIN_DESCARGA_CAMION_DISTRIBUCION: # en que momento calculo el tiempo que va a tardar en descargar
                    if stock_en_barraca <= PUNTO_DE_REORDEN:
                        duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                        nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_CARGA_REABASTECIMIENTO)
                        reloj += evento_actual.duracion
                    else:
                        duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                        nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_CARGA_BARRACA)
                        reloj += evento_actual.duracion
                
                elif evento_actual.nombre == ARRIBO_COLA_CARGA_REABASTECIMIENTO:
                    print(f'Evento: {ARRIBO_COLA_CARGA_REABASTECIMIENTO}')
                elif evento_actual.nombre == FIN_CARGA_CAMION_REABASTECIMIENTO:
                    duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo)
                    # setear el camion con el maximo de su carga
                    nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_DESCARGA_BARRACA)
                    reloj += evento_actual.duracion
                
                if not nuevo_evento is None:
                    eventos_futuros.append(nuevo_evento)
                    eventos_futuros = ordenar_eventos(eventos_futuros)

                # Eliminar el evento atendido
                    
                # aca tengo que avanzar el reloj
                # Cada vez que proceso el evento avanzo el reloj con el valor de demora del evento: reloj += evento.demora
                # Puede ocurrir que tenga que actualizar un contador o variable de estado, por ejemplo si estoy en el evento de fin de descarga del centro de distribucion, 
                # consulto en la barraca el stock  para saber si la tengo que reabastecer


if __name__ == '__main__':
    simulacion()
