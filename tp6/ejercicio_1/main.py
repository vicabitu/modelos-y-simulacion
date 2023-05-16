import numpy as np

def generarCantidadDemanda():
    MEDIA = 150
    DESVIO_ESTANDAR = 25
    return round(np.random.normal(loc=MEDIA, scale=DESVIO_ESTANDAR))
    

def simulacion():
    EXPERIMENTOS = 30
    CORRIDAS = 250
    CAPACIDAD_DE_PRODUCCION = 130
    PUNTO_DE_REORDEN = 50
    COSTO_CONSERVACION_UNIDAD = 70
    inventario = 90
    costos_anuales_de_mantenimiento = []
    turnos_adicionales = []

    for experimentos in range(EXPERIMENTOS): # años
        costo_anual_de_mantenimiento = 0
        turnos_anuales_adicionales = 0
        print(f'> Anio: {experimentos}')
        for corridas in range(CORRIDAS): # dias
            inventario += CAPACIDAD_DE_PRODUCCION
            cantidad_demandada = generarCantidadDemanda()
            inventario -= cantidad_demandada
            if inventario < PUNTO_DE_REORDEN:
                inventario += CAPACIDAD_DE_PRODUCCION
                turnos_anuales_adicionales += 1
            costo_anual_de_mantenimiento += (inventario * COSTO_CONSERVACION_UNIDAD)
        print(f'Cantidad de turnos adicionales: {turnos_anuales_adicionales}')
        print(f'Costo anual de mantenimiento: {costo_anual_de_mantenimiento}')
        print('---------------------------------------------')
        costos_anuales_de_mantenimiento.append(costo_anual_de_mantenimiento)
        turnos_adicionales.append(turnos_anuales_adicionales)
    
    promedio_de_costos_anuales_de_mantenimiento = np.mean(
        costos_anuales_de_mantenimiento
    )
    print(
        f'Promedio de costos anuales de mantenimiento: {round(promedio_de_costos_anuales_de_mantenimiento, 2)}'
    )
    promedio_de_turnos_adicionales = np.mean(turnos_adicionales)
    print(
        f'Promedio de turnos anuales adicionales: {round(promedio_de_turnos_adicionales, 1)}'
    )


if __name__ == '__main__':
    simulacion()
