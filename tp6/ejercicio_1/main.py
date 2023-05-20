import numpy as np

def confidence_interval(n_sample, mean, std, z_value=1.96, coeff=1.):
    # By default, it calculates the CI with a confidence level of 99%
    # Change `z_value` accordingly.
    # Optionally, use `coeff` to get a CI with a greater error margin
    z_term = coeff * (z_value * std / (n_sample ** 0.5))
    inf = mean - z_term
    sup = mean + z_term
    return inf, sup

def generarCantidadDemanda():
    MEDIA = 150
    DESVIO_ESTANDAR = 25
    return round(np.random.normal(loc=MEDIA, scale=DESVIO_ESTANDAR))
    

def simulacion():
    EXPERIMENTOS = 30
    CORRIDAS = 250
    CAPACIDAD_DE_PRODUCCION = 130
    COSTO_CONSERVACION_UNIDAD = 70
    inventario = 90
    costos_anuales_de_mantenimiento = []
    turnos_adicionales = []

    puntos_de_reorden = [50, 60, 70, 80]

    # Para el grafico hacer una lista con los costos de mantenimiento de los 30 anios y una lista con los promedios de los turnos adicionales por cada punto de reorden.

    for punto_de_reorden in puntos_de_reorden:
        print(f'Punto de reorden: {punto_de_reorden}')
        for experimentos in range(EXPERIMENTOS): # años
            costo_anual_de_mantenimiento = 0
            turnos_anuales_adicionales = 0
            for corridas in range(CORRIDAS): # dias
                inventario += CAPACIDAD_DE_PRODUCCION
                cantidad_demandada = generarCantidadDemanda()
                inventario -= cantidad_demandada
                if inventario < punto_de_reorden:
                    inventario += CAPACIDAD_DE_PRODUCCION
                    turnos_anuales_adicionales += 1
                costo_anual_de_mantenimiento += (inventario * COSTO_CONSERVACION_UNIDAD)
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

        desvio_estandar_de_costos_anuales_de_mantenimiento = np.std(costos_anuales_de_mantenimiento)
        cantidad_de_costos_anuales_de_mantenimiento = len(costos_anuales_de_mantenimiento)
        intervalo_de_confinanza = confidence_interval(
            cantidad_de_costos_anuales_de_mantenimiento,
            promedio_de_costos_anuales_de_mantenimiento,
            desvio_estandar_de_costos_anuales_de_mantenimiento
        )
        print('Intervalo de confianza:')
        print(f"Extermo inferior: {intervalo_de_confinanza[0]}")
        print(f"Extermo superior: {intervalo_de_confinanza[1]}")
        print('---------------------------------------------')
    
if __name__ == '__main__':
    simulacion()
