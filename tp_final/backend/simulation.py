import random

from models.camion import Camion
from models.evento import Evento
from models.planta import Planta
from models.balanza import Balanza
from models.puesto_de_carga import PuestoCargaDescarga
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

def generar_camiones():
    camiones = []
    for i in range(2):
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

def simulacion():
    EXPERIMENTOS = 1
    CORRIDAS = 5
    PUNTO_DE_REORDEN = 8000

    cantidad_materia_prima_en_planta = 0
    stock_en_barraca = 20000
    reloj = 0
    eventos_futuros = []
    cantidad_de_producto_terminada_en_planta = 0
    
    puesto_de_carga_barraca = PuestoCargaDescarga()
    puesto_de_descarga_barraca = PuestoCargaDescarga()
    puesto_de_descarga_planta = PuestoCargaDescarga()
    puesto_de_carga_planta = PuestoCargaDescarga()
    puesto_de_descarga_centro_distribucion = PuestoCargaDescarga()
    puesto_de_carga_centro_reabastecimiento = PuestoCargaDescarga()
    balanza_planta = Balanza()
    planta = Planta()

    cantidad_de_produccion_diaria = 0

    camiones = generar_camiones()
    eventos_futuros = ordenar_eventos(inicializar_eventos(camiones))
    for e in eventos_futuros:
        print(e)
    for experimentos in range(EXPERIMENTOS): #años
        reloj = 0
        cantidad_de_produccion_diaria = 0
        resetear_camiones(camiones)
        print('Comienzo')
        while len(eventos_futuros) > 0:
            nuevos_eventos = []
            evento_actual = eventos_futuros[0]
            print(f'Dia: {round(reloj/900)}')
            # Aca puede ser que venga el problema del loop infinito
            reloj = evento_actual.duracion
            print(f'> Reloj: {reloj}')
            print(f"Procesando: {evento_actual}")
            # Barraca:
            if evento_actual.nombre == ARRIBO_COLA_CARGA_BARRACA:
                puesto_de_carga_barraca.cola.append(evento_actual.objeto)
                print('Puesto de carga:')
                print(puesto_de_carga_barraca.mostrar_en_cola())
                if puesto_de_carga_barraca.libre:
                    nuevo_evento = puesto_de_carga_barraca.cargar_camion(reloj, FIN_CARGA_BARRACA)
                    nuevos_eventos.append(nuevo_evento)    

            elif evento_actual.nombre == FIN_CARGA_BARRACA:
                #print(f'Evento: FIN_CARGA_BARRACA')
                # puesto_de_carga_barraca.eliminar_camion(evento_actual.objeto) # Porque elimino el camion?
                # Deberia tomar un nuevo camion de la cola para que se pese?
                puesto_de_carga_barraca.liberar()
                nuevo_evento_1 = puesto_de_carga_barraca.cargar_camion(reloj, FIN_CARGA_BARRACA)

                camion = evento_actual.objeto
                stock_en_barraca -= camion.carga_neta
                nuevo_evento_2 = camion.viajar(reloj, materia_prima=True, nombre_evento=ARRIBO_COLA_PESAJE_PLANTA)
                
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])
                
            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_BARRACA:
                puesto_de_descarga_barraca.cola.append(evento_actual.objeto)
                print('Puesto de descarga:')
                print(puesto_de_descarga_barraca.mostrar_en_cola())
                if puesto_de_descarga_barraca.libre:
                    nuevo_evento = puesto_de_descarga_barraca.descargar_camion(reloj, FIN_DESCARGA_BARRACA)
                    nuevos_eventos.append(nuevo_evento)

            elif evento_actual.nombre == FIN_DESCARGA_BARRACA:
                stock_en_barraca += puesto_de_descarga_barraca.camion.carga_neta
                puesto_de_descarga_barraca.liberar()
                nuevo_evento = puesto_de_descarga_barraca.descargar_camion(reloj, FIN_DESCARGA_BARRACA)
                
                camion = evento_actual.objeto
                nuevo_evento = Evento(camion, reloj + 1, ARRIBO_COLA_CARGA_BARRACA)
                nuevos_eventos.append(nuevo_evento)

            # Planta:
            elif evento_actual.nombre == ARRIBO_COLA_PESAJE_PLANTA:
                balanza_planta.cola.append(evento_actual.objeto)
                print('Balanza en planta:')
                print(balanza_planta.mostrar_en_cola())
                if balanza_planta.libre:
                    nuevo_evento = balanza_planta.pesar_camion(reloj, FIN_PESAJE_PLANTA)
                    nuevos_eventos.append(nuevo_evento) 

            elif evento_actual.nombre == FIN_PESAJE_PLANTA:
                balanza_planta.liberar()
                nuevo_evento_1 = balanza_planta.pesar_camion(reloj, FIN_PESAJE_PLANTA)
                
                camion = evento_actual.objeto
                if camion.materia_prima:
                    nuevo_evento_2 = Evento(camion, reloj + 1, ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA)
                else:
                    nuevo_evento_2 = camion.viajar(reloj, camion.materia_prima, ARRIBO_COLA_DESCARGA_DISTRIBUCION)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])

            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA:
                #print(f'Evento: ARRIBO_COLA_DESCARGA_MATERIA_PRIMA_PLANTA')
                puesto_de_descarga_planta.cola.append(evento_actual.objeto)
                print('Puesto de descarga [Planta]:')
                print(puesto_de_descarga_planta.mostrar_en_cola())
                if puesto_de_descarga_planta.libre:
                    cantidad_materia_prima_en_planta += evento_actual.objeto.carga_neta
                    nuevo_evento = puesto_de_descarga_planta.descargar_camion(reloj, FIN_DESCARGA_MATERIA_PRIMA_PLANTA)
                    nuevos_eventos.append(nuevo_evento)

            elif evento_actual.nombre == FIN_DESCARGA_MATERIA_PRIMA_PLANTA:
                #print(f'Evento: FIN_DESCARGA_MATERIA_PRIMA_PLANTA')
                puesto_de_descarga_planta.liberar()
                nuevo_evento_1 = puesto_de_descarga_planta.descargar_camion(reloj, FIN_DESCARGA_MATERIA_PRIMA_PLANTA)
                camion = evento_actual.objeto
                camion.vaciar()
                nuevo_evento_2 = Evento(camion, reloj + 1, ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO)
                nuevos_eventos.extend([nuevo_evento_1, nuevo_evento_2])

                # acá comienza la producción
                if cantidad_materia_prima_en_planta >= CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR and planta.libre: #Empiezo a producir
                    ciclos_completos, ciclos_incompletos = planta.calcular_ciclos(cantidad_materia_prima_en_planta)
                    cantidad_materia_prima_en_planta -= ciclos_completos * 1000 # la cantidad de materia prima es igual a la cantidad de ciclos de producción porque 1.1 ton produce 1 ton
                    cantidad_de_producto_terminada_en_planta += ciclos_completos * 1000
                    inicio = reloj
                    for ciclo in range(ciclos_completos):
                        nuevo_evento = planta.producir(inicio)
                        duracion_previa = nuevo_evento.duracion
                        nuevos_eventos.append(nuevo_evento)
                        if ciclo > 0:
                            inicio += duracion_previa

            elif evento_actual.nombre == FIN_PRODUCCION_PLANTA:
                #print(f'Evento: FIN_PRODUCCION_PLANTA')
                planta.liberar()
                nuevo_evento = puesto_de_carga_planta.cargar_camion(reloj, FIN_CARGA_PRODUCTO_TERMINADO)
                nuevos_eventos.append(nuevo_evento)
                
            elif evento_actual.nombre == ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO:
                #print(f'Evento: ARRIBO_COLA_CARGA_PRODUCTO_TERMINADO')
                puesto_de_carga_planta.cola.append(evento_actual.objeto)
                print('Puesto de carga [Planta]:')
                print(puesto_de_carga_planta.mostrar_en_cola())
                if puesto_de_carga_planta.libre and cantidad_de_producto_terminada_en_planta > 0:
                    nuevo_evento_1 = puesto_de_carga_planta.cargar_camion(reloj, FIN_CARGA_PRODUCTO_TERMINADO)
                    # Aca le doy el producto que puedo, todo o una parte
                    if cantidad_de_producto_terminada_en_planta <= nuevo_evento_1.objeto.carga_neta:
                        nuevo_evento_1.objeto.carga_neta = cantidad_de_producto_terminada_en_planta
                    cantidad_de_producto_terminada_en_planta -= nuevo_evento_1.objeto.carga_neta
                    nuevos_eventos.append(nuevo_evento)

            elif evento_actual.nombre == FIN_CARGA_PRODUCTO_TERMINADO:
                #print(f'Evento: FIN_CARGA_PRODUCTO_TERMINADO')
                puesto_de_carga_planta.liberar()
                camion = evento_actual.objeto
                cantidad_de_producto_terminada_en_planta -= camion.carga_neta
                camion.materia_prima = False

                nuevo_evento = Evento(camion, reloj + 1, ARRIBO_COLA_PESAJE_PLANTA)
                nuevos_eventos.append(nuevo_evento)

            # Centro de distribucion
            elif evento_actual.nombre == ARRIBO_COLA_DESCARGA_DISTRIBUCION:
                #print(f'Evento: ARRIBO_COLA_DESCARGA_DISTRIBUCION')
                puesto_de_descarga_centro_distribucion.cola.append(evento_actual.objeto)
                print('Puesto de descarga [Planta]:')
                print(puesto_de_descarga_centro_distribucion.mostrar_en_cola())
                if puesto_de_descarga_centro_distribucion.libre:
                    cantidad_de_produccion_diaria += puesto_de_descarga_centro_distribucion.camion.carga_neta # calculo para las estadisticas
                    nuevo_evento = puesto_de_descarga_centro_distribucion.descargar_camion(reloj, FIN_DESCARGA_CAMION_DISTRIBUCION)
                    nuevos_eventos.append(nuevo_evento)

            elif evento_actual.nombre == FIN_DESCARGA_CAMION_DISTRIBUCION:
                #print(f'Evento: FIN_DESCARGA_CAMION_DISTRIBUCION')
                camion = puesto_de_descarga_centro_distribucion.camion
                puesto_de_descarga_centro_distribucion.liberar()
                puesto_de_descarga_centro_distribucion.descargar_camion(reloj)
                if stock_en_barraca <= PUNTO_DE_REORDEN:
                    nuevo_evento = camion.viajar(reloj, materia_prima=False, nombre_evento=ARRIBO_COLA_CARGA_REABASTECIMIENTO)
                else:
                    nuevo_evento = camion.viajar(reloj, materia_prima=False, nombre_evento=ARRIBO_COLA_CARGA_BARRACA)
                nuevos_eventos.append(nuevo_evento)

            # Centro reabastecimiento
            elif evento_actual.nombre == ARRIBO_COLA_CARGA_REABASTECIMIENTO:
                #print(f'Evento: ARRIBO_COLA_CARGA_REABASTECIMIENTO')
                puesto_de_carga_centro_reabastecimiento.cola.append(evento_actual.objeto)
                print('Puesto de carga [Reabastecimiento]:')
                print(puesto_de_carga_centro_reabastecimiento.mostrar_en_cola())
                if puesto_de_carga_centro_reabastecimiento.libre:
                    nuevo_evento = puesto_de_carga_centro_reabastecimiento.reabastecer_camion(reloj)
                    nuevos_eventos.append(nuevo_evento)

            elif evento_actual.nombre == FIN_CARGA_CAMION_REABASTECIMIENTO:
                #print(f'Evento: FIN_CARGA_CAMION_REABASTECIMIENTO')
                puesto_de_carga_centro_reabastecimiento.liberar()
                camion = evento_actual.objeto
                nuevo_evento = camion.viajar(reloj, materia_prima=True, nombre_evento=ARRIBO_COLA_DESCARGA_BARRACA)
                nuevos_eventos.append(nuevo_evento)
            
            #print(f'Reloj al final: {reloj}')
            print("-"* 40)
            
            # Elimino los eventos futuros que son None
            nuevos_eventos = [e for e in nuevos_eventos if e is not None]
            eventos_futuros.extend(nuevos_eventos)
            eventos_futuros.remove(evento_actual)
            eventos_futuros = ordenar_eventos(eventos_futuros)

            if round(reloj / 900) == CORRIDAS + 1:
                # Corto el bucle while de los dias
                break

        print('Fin corridas')

if __name__ == '__main__':
    simulacion()
