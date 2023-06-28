CANTIDAD_MATERIA_PRIMA_PARA_PRODUCIR = 1100
N_CAMIONES = 15 #3
MINS_SIMULACION = 120 #120 900
STOCK_EN_BARRACA = 20000

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

FIN_PRODUCCION_PLANTA = 'FPRP'
# Centro de distribucion
ARRIBO_COLA_DESCARGA_DISTRIBUCION = 'ACDD'
FIN_DESCARGA_CAMION_DISTRIBUCION = 'FDCD'
# Centro reabastecimiento
ARRIBO_COLA_CARGA_REABASTECIMIENTO = 'ACCR'
FIN_CARGA_CAMION_REABASTECIMIENTO = 'FCCR'



TIEMPOS_DE_VIAJE = {
    1: {
        'media': 29,
        'desvio': 5.1
    },
    2: {
        'media': 30,
        'desvio': 6.4
    },
    3: {
        'media': 35,
        'desvio': 8
    },
    4: {
        'media': 38,
        'desvio': 12.3
    },
}

PESAJES_CAMIONES = {
    1: {
        'media': 34,
        'desvio': 3
    },
    2: {
        'media': 27.5,
        'desvio': 2
    },
    3: {
        'media': 40,
        'desvio': 1.1
    },
    4: {
        'media': 49,
        'desvio': 0.7
    },
}

TIEMPOS_CARGA_DESCARGA = {
    1: 23,
    2: 20,
    3: 28,
    4: 35,
}

PESO_CAMIONES = {
    1: {
        'sin_carga': 31,
        'peso_maximo': 38
    },
    2: {
        'sin_carga': 25,
        'peso_maximo': 30
    },
    3: {
        'sin_carga': 37,
        'peso_maximo': 44
    },
    4: {
        'sin_carga': 43,
        'peso_maximo': 52
    },
}
