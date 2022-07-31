# Constantes
"""Valor 'Infinito'"""
max_Int=2**63-1

# Definicion de Funciones

# Funciones de graficación
def pintar_grafo():
    """Funcion para pintar en consola, con objetivo de pruebas"""
    pass

# Funciones de apoyo
def convertir_grid(grid):
    """Funcion para convertir un grid de pesos en un grafo (diccionario de nodos)"""
    grafo = {}
    direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for i, fila in enumerate(grid):
        for j, columna in enumerate(fila):
            nodos_vecinos = []
            for x, y in direcciones:
                newx, newy = x+i, y+j
                if 0 <= newx < len(fila) and 0 <= newy < len(grid):
                    nodos_vecinos.append(((newx, newy), grid[newx][newy]))
            grafo[(i, j)] = nodos_vecinos
    return grafo

# Algoritmos de caminos minimos
def Dijkstra(inicio,final,mAd):
    """Primera version de algoritmo que utiliza una matriz de adyacencia
    y un valor maximo para obtener el camino minimo"""
    # Variables
    costo_minimo=len(mAd)*[max_Int]
    recorrido_minimo=len(mAd)*[0]
    nodos_visitados=len(mAd)*[False]
    nodo_actual=inicio
    costo_minimo[nodo_actual]=0
    # Proceso
    # Bucle con limite que recorrera como maximo todos los nodos del grafo para hallar el camino minimo
    for n in range(len(mAd)):
        nodos_visitados[nodo_actual] = True
        if nodo_actual==final: # Detener bucle si ya se alcanzo el nodo final
            break
        for i in range(len(mAd)):
            if costo_minimo[nodo_actual] < costo_minimo[i]-mAd[nodo_actual][i]: # Actualizar lista de costos minimos
                costo_minimo[i]=costo_minimo[nodo_actual]+mAd[nodo_actual][i]
                recorrido_minimo[i]=nodo_actual
        min=max_Int
        for i in range(len(mAd)):
            if not nodos_visitados[i] and costo_minimo[i]<min: # Elegir un nuevo nodo a evaluar segun el minimo costo
                nodo_actual=i
                min=costo_minimo[i]
    camino=""
    for n in range(len(mAd)):
        camino+=str(nodo_actual+1) #Crear un nuevo formato para la visualizacion del código
        if nodo_actual==inicio:
            break
        nodo_actual=recorrido_minimo[nodo_actual]
        camino+=","
    camino=camino[::-1]
    return camino

def Dijkstra_v2(inicio,final,grafo):
    """Segunda version de algoritmo que utiliza un diccionario con los nodos del grafo
    para hallar la lista de nodos(puntos) que conforman el camino minimo. No requiere
    un tamaño maximo o 'infinito'."""
    # Variables
    costo_minimo = {inicio: 0}
    recorrido_de_nodos = {inicio: None}
    nodos_visitados = []
    nodo_actual = inicio
    # Proceso
    # Bucle con limite que recorrera como maximo todos los nodos del grafo para hallar el camino minimo
    while nodo_actual is not None:
        nodos_visitados.append(nodo_actual)
        if nodo_actual == final:  # Detener bucle si ya se alcanzo el nodo final
            break
        for nodo_vecino in grafo[nodo_actual]:
            punto_vecino, costo_de_vecino = nodo_vecino
            if punto_vecino not in costo_minimo or costo_minimo[nodo_actual]+costo_de_vecino < costo_minimo[punto_vecino]:
                costo_minimo[punto_vecino] = costo_minimo[nodo_actual]+costo_de_vecino
                recorrido_de_nodos[punto_vecino] = nodo_actual
        min = None
        nodo_actual = None
        for nodo in costo_minimo:
            if nodo not in nodos_visitados:
                min = costo_minimo[nodo] if min is None else min
                if costo_minimo[nodo] <= min:  # Elegir un nuevo nodo a evaluar segun el minimo costo
                    min = costo_minimo[nodo]
                    nodo_actual = nodo
    camino = []
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual=recorrido_de_nodos[nodo_actual]
    return camino[::-1]
