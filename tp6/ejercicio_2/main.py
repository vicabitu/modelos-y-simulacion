import numpy as np
import random

CANTIDAD_A_ORDENAR = 100

def generar_tiempo_de_espera(numero_aleatorio):
    tiempo_de_espera = None
    
    limites = [0.4, 0.6, 0.75, 0.90, 1.0]
    tiempos = [1, 2, 3, 4, 5]
    
    for i in range(len(limites)):
        if numero_aleatorio <= limites[i]:
            tiempo_de_espera = tiempos[i]
            break
    return tiempo_de_espera

def generar_tiempo_de_entrega(numero_aleatorio):
    tiempo_de_entrega = None
    
    limites = [0.2, 0.5, 0.75, 1.0]
    tiempos = [1, 2, 3, 4]
    
    for i in range(len(limites)):
        if numero_aleatorio <= limites[i]:
            tiempo_de_entrega = tiempos[i]
            break
    return tiempo_de_entrega

def generar_demanda(numero_aleatorio):
    demanda_diaria = None
    
    limites = [0.2, 0.24, 0.3, 0.42, 0.62, 0.65, 0.8, 0.9, 1.0]
    demandas = [25, 30, 40, 50, 100, 150, 200, 250, 300]
    
    for i in range(len(limites)):
        if numero_aleatorio <= limites[i]:
            demanda_diaria = demandas[i]
            break
    return demanda_diaria

def generar_pedido_para_un_cliente(demanda):
    numero_aleatorio = random.random()
    tiempo_de_entrega = generar_tiempo_de_entrega(numero_aleatorio)
    return [tiempo_de_entrega, demanda]

def generar_pedido_de_lote():
    numero_aleatorio = random.random()
    tiempo_de_espera = generar_tiempo_de_espera(numero_aleatorio)
    return [tiempo_de_espera, CANTIDAD_A_ORDENAR]

def procesar_pedidos_pendientes_de_entrega(pedidos_pendientes):
    cantidad_de_inventario_a_decrementar = 0
    if len(pedidos_pendientes):
        np_pedidos_pendientes = np.array(pedidos_pendientes)
        # A todos los pedidos les decremento en uno el dia de espera de entrega
        np_pedidos_pendientes[:, 0] = np_pedidos_pendientes[:, 0] - 1
        # Me quedo con los pedidos que ya cumplieron con el tiempo de entrega
        pedidos_listos_para_entregar = np_pedidos_pendientes[
            np_pedidos_pendientes[:, 0] == 0
        ]
        cantidad_de_inventario_a_decrementar = np.sum(
            pedidos_listos_para_entregar[:, 1]
        )
        # Me quedo con los pedidos que todavia me falta entregar
        pedidos_pendientes = np_pedidos_pendientes[
            np_pedidos_pendientes[:, 0] != 0
        ].tolist()
    return [cantidad_de_inventario_a_decrementar, pedidos_pendientes]

def procesar_pedidos_pendientes_de_espera(pedidos_pendientes):
    cantidad_de_inventario_a_incrementar = 0
    if len(pedidos_pendientes):
        np_pedidos_pendientes = np.array(pedidos_pendientes)
        # A todos los pedidos les decremento en uno el dia de espera de espera
        np_pedidos_pendientes = np_pedidos_pendientes[:, 0] - 1
        lotes_listos = np_pedidos_pendientes[
            np_pedidos_pendientes[:, 0] == 0
        ]
        cantidad_de_inventario_a_incrementar = np.sum(lotes_listos[:, 1])
        pedidos_pendientes = np_pedidos_pendientes[
            np_pedidos_pendientes[:, 0] != 0
        ].tolist()
    return [cantidad_de_inventario_a_incrementar, pedidos_pendientes]

def simulacion():
    print('Simulacion')
    CORRIDAS = 15
    COSTO_CONSERVACION_UNIDAD = 450
    COSTO_DE_ORDENAR = 3800
    COSTO_DE_FALTANTE = 625
    PUNTO_DE_REORDEN = 15
    COSTO_COMPRA_UNIDAD = 950
    inventario = 1500

    # Salidas
    costo_total_de_ordenar = 0 #(K)
    costo_total_de_conservacion = 0 #(H)
    costo_total_de_compra = 0 #(C)
    costo_total_de_faltantes = 0 #(B)

    # Variables de estado
    pedidos_pendientes_de_entrega = []
    pedidos_pendientes_de_espera = []

    for corridas in range(CORRIDAS): # dias
        print(f'Inventario al inicio: {inventario}')

        cantidad_de_inventario_a_decrementar, pedidos_pendientes_de_entrega = procesar_pedidos_pendientes_de_entrega(
            pedidos_pendientes_de_entrega
        )
        inventario -= cantidad_de_inventario_a_decrementar
        print(
            f'Cantidad a decrementar: {cantidad_de_inventario_a_decrementar} - Inventario: {inventario}'
        )

        cantidad_de_inventario_a_incrementar, pedidos_pendientes_de_espera = procesar_pedidos_pendientes_de_espera(
            pedidos_pendientes_de_espera
        )
        inventario += cantidad_de_inventario_a_incrementar
        print(
            f'Cantidad a incrementar: {cantidad_de_inventario_a_incrementar} - Inventario: {inventario}'
        )
        
        numero_aleatorio = random.random()
        demanda = generar_demanda(numero_aleatorio)
        print(f'Demanda: {demanda}')
        if demanda <= inventario:
            print('Puedo cubrir toda la demanda')
            pedido_cliente = generar_pedido_para_un_cliente(demanda)
            pedidos_pendientes_de_entrega.append(pedido_cliente)
            costo_total_de_conservacion += (inventario * COSTO_CONSERVACION_UNIDAD) # ojo aca si el inventario es cero!
            # Verificar punto de reorden, lo tomo como lo que ya me compraron, por
            # mas que no todavia no lo entregue no lo tengo disponible en el inventario
            if (inventario - demanda) == PUNTO_DE_REORDEN:
                print('Punto de reorden')
                pedido_de_lote = generar_pedido_de_lote()
                pedidos_pendientes_de_espera.append(pedido_de_lote)
                costo_total_de_ordenar += COSTO_DE_ORDENAR
                costo_total_de_compra += (CANTIDAD_A_ORDENAR * COSTO_COMPRA_UNIDAD )
        else:
            print('No puedo cubrir toda la demanda')
            print(f'Inventario: {inventario}')
            if inventario > 0:
                print(f'Cantidad cubierta: {inventario}')
                print(f'Cantidad faltante: {demanda - inventario}')
                costo_total_de_faltantes += ((demanda - inventario) * COSTO_DE_FALTANTE)
                pedido_cliente = generar_pedido_para_un_cliente(inventario)
                pedidos_pendientes_de_entrega.append(pedido_cliente)
            else:
                print('No hay inventario disponible')
        print(f'>Costo de ordenar: {costo_total_de_ordenar}')
        print(f'Costo de conservacion: {costo_total_de_conservacion}')
        print(f'Costo total de la compra: {costo_total_de_compra}')
        print(f'Costo total de faltantes: {costo_total_de_faltantes}')
        print('Pedidos pendientes de entrega:')
        print(pedidos_pendientes_de_entrega)
        print('Pedidos pendientes de espera')
        print(pedidos_pendientes_de_espera)
        print('--------------------------------------------')

if __name__ == '__main__':
    simulacion()
