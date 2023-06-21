import random
import numpy as np

from models.camion import Camion
from models.evento import Evento
from models.recurso import Recurso
from models.planta import Planta
from constants import (
    TIEMPOS_DE_VIAJE,
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
    for i in range(2):
        numero_aleatorio = random.random()
        tipo_de_camion = generar_tipo_de_camion(numero_aleatorio)
        camion = Camion(tipo_de_camion, i)
        camiones.append(camion)
    return camiones

def calcular_tiempo_de_viaje_segun_tipo_de_camion(tipo_de_camion):
    media = TIEMPOS_DE_VIAJE.get(tipo_de_camion).get('media')
    desvio = TIEMPOS_DE_VIAJE.get(tipo_de_camion).get('desvio')
    return round(np.random.normal(loc=media, scale=desvio))

def calcular_tiempo_de_produccion_de_planta():
    return 10 + round(np.random.exponential(scale=5))

def obtener_tiempo_carga_descarga_segun_tipo_de_camion(tipo_de_camion):
    print(f'Tiempo de carga/descarga: {TIEMPOS_CARGA_DESCARGA.get(tipo_de_camion)}')
    return TIEMPOS_CARGA_DESCARGA.get(tipo_de_camion)

def ordenar_eventos(eventos):
    return sorted(eventos, key=lambda evento: evento.duracion)

def calcular_tiempo_de_pesaje_de_camion():
    return round(np.random.normal(loc=11, scale=3))

def inicializar_eventos(camiones):
    eventos = []
    for camion in camiones:
        duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(camion.tipo)
        evento = Evento(camion, duracion, ARRIBO_COLA_CARGA_BARRACA)
        eventos.append(evento)
    return eventos

def resetear_camiones(camiones):
    for c in camiones:
        c.carga_neta = 0

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
    puesto_de_descarga_centro_distribucion = Recurso()
    puesto_de_carga_centro_reabastecimiento = Recurso()
    balanza_planta = Recurso('Balanza')
    planta = Planta()

    cantidad_de_produccion_diaria = 0

    camiones = generar_camiones()
    eventos_futuros = ordenar_eventos(inicializar_eventos(camiones))
    for e in eventos_futuros:
        print(e)
    for experimentos in range(EXPERIMENTOS): #años
        # for corridas in range(CORRIDAS): #dias
        reloj = 0
        cantidad_de_produccion_diaria = 0
        nuevos_eventos = []
        resetear_camiones(camiones)
        print('Comienzo')
        while True:
            evento_actual = eventos_futuros[0]
            print(f'Dia: {round(reloj/900)}')
            print(f'> Reloj al inicio: {reloj}')
            # Aca puede ser que venga el problema del loop infinito
            reloj = evento_actual.duracion
            print(f'Duracion evento actual: {evento_actual.duracion}')
            # Barraca:
            if evento_actual.nombre == ARRIBO_COLA_CARGA_BARRACA:
                print(f'Evento: ARRIBO_COLA_CARGA_BARRACA')
                if puesto_de_carga_barraca.libre:
                    print('if')
                    puesto_de_carga_barraca.cola.append(evento_actual.objeto)
                    camion = puesto_de_carga_barraca.cola.pop(0)
                    puesto_de_carga_barraca.camion = camion
                    puesto_de_carga_barraca.libre = False
                    camion.set_carga()
                    duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion.tipo) + reloj
                    nuevo_evento = Evento(camion, duracion, FIN_CARGA_BARRACA)
                    nuevos_eventos.append(nuevo_evento)
                    print('Puesto de carga:')
                    print(puesto_de_carga_barraca)
                    print('Camion que ingresa a la cola:')
                    print(camion)
                    print(f'Duracion: {duracion}')
                    print('Nuevo evento:')
                    print(nuevo_evento)
                else:
                    print('else')
                    puesto_de_carga_barraca.cola.append(evento_actual.objeto)
                    print('Puesto de carga:')
                    print(puesto_de_carga_barraca)
            elif evento_actual.nombre == FIN_CARGA_BARRACA:
                print(f'Evento: FIN_CARGA_BARRACA')
                # puesto_de_carga_barraca.eliminar_camion(evento_actual.objeto) # Porque elimino el camion?
                # Deberia tomar un nuevo camion de la cola para que se pese?
                camion = evento_actual.objeto
                puesto_de_carga_barraca.libre = True
                stock_en_barraca -= camion.carga_neta
                duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(camion.tipo) + reloj
                nuevo_evento = Evento(camion, duracion, ARRIBO_COLA_PESAJE_PLANTA)
                nuevos_eventos.append(nuevo_evento)
                camion.materia_prima = True
                print('Puesto de carga:')
                print(puesto_de_carga_barraca)
                print(f'Duracion: {duracion}')
                print('Nuevo evento:')
                print(nuevo_evento)
            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_BARRACA:
                print(f'Evento: ARRIBO_COLA_DESCARGA_BARRACA')
                if puesto_de_descarga_barraca.libre:
                    puesto_de_descarga_barraca.cola.append(nuevo_evento.objeto)
                    camion = puesto_de_descarga_barraca.cola.pop(0)
                    puesto_de_descarga_barraca.camion = camion
                    puesto_de_descarga_barraca.libre = False
                    duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion) + reloj
                    nuevo_evento = Evento(camion, duracion, FIN_DESCARGA_BARRACA)
                    nuevos_eventos.append(nuevo_evento)
                else:
                    puesto_de_descarga_barraca.cola.append(evento_actual.objeto)
            elif evento_actual.nombre == FIN_DESCARGA_BARRACA:
                print(f'Evento: FIN_DESCARGA_BARRACA')
                stock_en_barraca += evento_actual.objeto.carga_neta
                evento_actual.objeto.carga_neta = 0
                nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_CARGA_BARRACA)
                nuevos_eventos.append(nuevo_evento)
                puesto_de_descarga_barraca.libre = True
            # Planta:
            elif evento_actual.nombre == ARRIBO_COLA_PESAJE_PLANTA:
                print(f'Evento: ARRIBO_COLA_PESAJE_PLANTA')
                if balanza_planta.libre:
                    balanza_planta.cola.append(nuevo_evento.objeto)
                    camion = balanza_planta.cola.pop(0)
                    balanza_planta.camion = camion
                    balanza_planta.libre = False
                    duracion = calcular_tiempo_de_pesaje_de_camion() + reloj
                    # balanza_planta.eliminar_camion(evento_actual.objeto)
                    nuevo_evento = Evento(camion, duracion, FIN_PESAJE_PLANTA)
                    nuevos_eventos.append(nuevo_evento)
                    print('Balanza:')
                    print(balanza_planta)
                    print('Camion que ingresa a la balanza:')
                    print(camion)
                    print(f'Duracion: {duracion}')
                    print('Nuevo evento:')
                    print(nuevo_evento)
                else:
                    balanza_planta.cola.append(evento_actual.objeto)
            elif evento_actual.nombre == FIN_PESAJE_PLANTA:
                print(f'Evento: FIN_PESAJE_PLANTA')
                balanza_planta.libre = True
                if evento_actual.objeto.materia_prima:
                    nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA)
                else: 
                    duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo) + reloj
                    nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_DESCARGA_DISTRIBUCION)
                nuevos_eventos.append(nuevo_evento)
            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA:
                print(f'Evento: ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA')
                if puesto_de_descarga_planta.libre:
                    puesto_de_descarga_planta.cola.append(nuevo_evento.objeto)
                    camion = puesto_de_descarga_planta.cola.pop(0)
                    puesto_de_descarga_planta.camion = camion
                    puesto_de_carga_planta.libre = False
                    duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(evento_actual.objeto.tipo) + reloj
                    nuevo_evento = Evento(evento_actual.objeto, duracion, FIN_DESCARGA_MATERIA_PRIMA_PLANTA)
                    nuevos_eventos.append(nuevo_evento)
                else:
                    puesto_de_descarga_planta.cola.append(evento_actual.objeto)
            elif evento_actual.nombre == FIN_DESCARGA_MATERIA_PRIMA_PLANTA:
                print(f'Evento: FIN_DESCARGA_MATERIA_PRIMA_PLANTA')
                cantidad_materia_prima_en_planta += evento_actual.objeto.carga_neta
                evento_actual.objeto.carga_neta = 0
                nuevo_evento = Evento(evento_actual.objeto, reloj + 1, ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO)
                nuevos_eventos.append(nuevo_evento)
                puesto_de_descarga_planta.libre = True
                if cantidad_materia_prima_en_planta >= CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR and planta.libre: #Empiezo a producir
                    duracion = calcular_tiempo_de_produccion_de_planta() + reloj
                    nuevo_evento = Evento(planta, duracion, FIN_PRODUCCION_PLANTA)
                    nuevos_eventos.append(nuevo_evento)
                    planta.libre = False
                
            elif evento_actual.nombre == ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO:
                print(f'Evento: ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO')
                # Aca deberia preguntar si hay producto terminado?
                if cantidad_de_producto_terminada_en_planta > 0:
                    if puesto_de_carga_planta.libre:
                        puesto_de_carga_planta.cola.append(nuevo_evento.objeto)
                        camion = puesto_de_carga_planta.cola.pop(0)
                        puesto_de_carga_planta.camion = camion
                        camion.set_carga()
                        duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion) + reloj
                        nuevo_evento = Evento(camion, duracion, FIN_CARGA_PRODUCTO_TERMINADO)
                        nuevos_eventos.append(nuevo_evento)
                    else:
                        puesto_de_carga_planta.cola.append(nuevo_evento.objeto)
            elif evento_actual.nombre == FIN_CARGA_PRODUCTO_TERMINADO:
                print(f'Evento: FIN_CARGA_PRODUCTO_TERMINADO')
                camion = evento_actual.objeto
                nuevo_evento = Evento(camion, reloj + 1, ARRIBO_COLA_PESAJE_PLANTA)
                nuevos_eventos.append(nuevo_evento)
                puesto_de_carga_planta.libre = True
                cantidad_de_producto_terminada_en_planta -= nuevo_evento.objeto.carga_neta
                camion.materia_prima = False
            elif evento_actual.nombre == FIN_PRODUCCION_PLANTA:
                print(f'Evento: FIN_PRODUCCION_PLANTA')
                planta.libre = True
                cantidad_de_producto_terminada_en_planta += 10000
                if len(puesto_de_carga_planta.cola) > 0 and puesto_de_carga_planta.libre:
                    camion = puesto_de_carga_planta.cola.pop(0)
                    duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion) + reloj
                    nuevo_evento = Evento(camion, duracion, FIN_CARGA_PRODUCTO_TERMINADO)
                    nuevos_eventos.append(nuevo_evento)
            # Centro de distribucion
            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_DISTRIBUCION:
                print(f'Evento: ARRIBO_COLA_DESCARGA_DISTRIBUCION')
                # Puesto de descarga libre o ocupado
                if puesto_de_descarga_centro_distribucion.libre:
                    cantidad_de_produccion_diaria += evento_actual.objeto.carga_neta # calculo para las estadisticas
                    puesto_de_descarga_centro_distribucion.cola.append(nuevo_evento.objeto)
                    camion = puesto_de_descarga_centro_distribucion.cola.pop(0)
                    puesto_de_descarga_centro_distribucion.camion = camion
                    camion.carga_neta = 0
                    duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion) + reloj
                    nuevo_evento = Evento(camion, duracion, FIN_DESCARGA_CAMION_DISTRIBUCION)
                    nuevos_eventos.append(nuevo_evento)
                else:
                    puesto_de_descarga_centro_distribucion.cola.append(evento_actual.objeto)
            elif evento_actual.nombre == FIN_DESCARGA_CAMION_DISTRIBUCION: # en que momento calculo el tiempo que va a tardar en descargar
                print(f'Evento: FIN_DESCARGA_CAMION_DISTRIBUCION')
                if stock_en_barraca <= PUNTO_DE_REORDEN:
                    duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo) + reloj
                    nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_CARGA_REABASTECIMIENTO)
                else:
                    duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(evento_actual.objeto.tipo) + reloj
                    nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_CARGA_BARRACA)
                nuevos_eventos.append(nuevo_evento)
                puesto_de_descarga_centro_distribucion.libre = True
            # Centro reabastecimiento
            elif evento_actual.nombre == ARRIBO_COLA_CARGA_REABASTECIMIENTO:
                print(f'Evento: ARRIBO_COLA_CARGA_REABASTECIMIENTO')
                if puesto_de_carga_centro_reabastecimiento.libre:
                    puesto_de_carga_centro_reabastecimiento.cola.append(nuevo_evento.objeto)
                    camion = puesto_de_carga_centro_reabastecimiento.cola.pop(0)
                    puesto_de_carga_centro_reabastecimiento.camion = camion
                    camion.cargar_al_maximo()
                    duracion = obtener_tiempo_carga_descarga_segun_tipo_de_camion(camion) + reloj
                    nuevo_evento = Evento(camion, duracion, FIN_CARGA_CAMION_REABASTECIMIENTO)
                    nuevos_eventos.append(nuevo_evento)
                else:
                    puesto_de_carga_centro_reabastecimiento.cola.append(evento_actual.objeto)
            elif evento_actual.nombre == FIN_CARGA_CAMION_REABASTECIMIENTO:
                print(f'Evento: FIN_CARGA_CAMION_REABASTECIMIENTO')
                camion = evento_actual.objeto
                duracion = calcular_tiempo_de_viaje_segun_tipo_de_camion(camion.tipo) + reloj
                nuevo_evento = Evento(evento_actual.objeto, duracion, ARRIBO_COLA_DESCARGA_BARRACA)
                nuevos_eventos.append(nuevo_evento)
                puesto_de_carga_centro_reabastecimiento.libre = True
                camion.materia_prima = True
            
            print(f'Reloj al final: {reloj}')
            
            for e in nuevos_eventos:
                eventos_futuros.append(e)

            eventos_futuros.remove(evento_actual)
            eventos_futuros = ordenar_eventos(eventos_futuros)

            if round(reloj / 900) == CORRIDAS + 1:
                # Corto el bucle while de los dias
                break

        print('Fin corridas')

if __name__ == '__main__':
    simulacion()
