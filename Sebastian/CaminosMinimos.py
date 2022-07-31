# Constantes
"""Valor 'Infinito'"""
max_Int=2**63-1

# Definicion de Funciones

# Funciones de graficación
def pintar_grafo_en_consola(grid):
    """Funcion para pintar en consola, con objetivo de pruebas.
    I = punto de inicio, F = punto final, V = nodos visitados, C = camino minimo"""
    RESETEAR = "\033[1;0m"
    BLOQUE_AMARILLO = "\033[1;103m"
    BLOQUE_VERDE = "\033[1;102m"
    BLOQUE_AZUL = "\033[1;104m"
    BLOQUE_VERDEOSCURO = "\033[1;42m"
    BLOQUE_PARED = "\033[1;107m"
    for fil in range(len(grid)):
        for col in range(len(grid[fil])):
            peso, signo = grid[fil][col]
            COLOR = BLOQUE_AMARILLO if peso == 1 else BLOQUE_VERDE if peso == 2 else BLOQUE_AZUL if peso == 3 else \
                BLOQUE_VERDEOSCURO if peso == 4 else BLOQUE_PARED if peso == 5 else ""
            print(COLOR,signo,RESETEAR,sep="",end=" ")
        print()
    pass

def limpiar_consola():
    print("\033c",sep="",end="")

# Funciones de apoyo
def convertir_grid(grid):
    """Funcion para convertir un grid de pesos en un grafo (diccionario de nodos)."""
    grafo = {}
    direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for j, fila in enumerate(grid):
        for i, columna in enumerate(fila):
            if grid[j][i] < 5:
                nodos_vecinos = []
                for x, y in direcciones:
                    newx, newy = x+i, y+j
                    if 0 <= newx < len(fila) and 0 <= newy < len(grid) and grid[newy][newx]!= 5:
                        nodos_vecinos.append(((newx, newy), grid[newy][newx]))
                grafo[(i, j)] = nodos_vecinos
    return grafo

# Algoritmos de caminos minimos
def Dijkstra(inicio,final,mAd):
    """Primera version de algoritmo que utiliza una matriz de adyacencia
    y un valor maximo para obtener el camino minimo."""
    # Variables
    costo_minimo = len(mAd)*[max_Int]
    recorrido_minimo = len(mAd)*[0]
    nodos_visitados = len(mAd)*[False]
    nodo_actual = inicio
    costo_minimo[nodo_actual] = 0
    # Proceso
    # Bucle con limite que recorrera como maximo todos los nodos del grafo para hallar el camino minimo
    for n in range(len(mAd)):
        nodos_visitados[nodo_actual] = True
        if nodo_actual == final:  # Detener bucle si ya se alcanzo el nodo final
            break
        for i in range(len(mAd)):
            if costo_minimo[nodo_actual] < costo_minimo[i]-mAd[nodo_actual][i]: # Actualizar lista de costos minimos
                costo_minimo[i] = costo_minimo[nodo_actual]+mAd[nodo_actual][i]
                recorrido_minimo[i] = nodo_actual
        min = max_Int
        for i in range(len(mAd)):
            if not nodos_visitados[i] and costo_minimo[i] < min: # Elegir un nuevo nodo a evaluar segun el minimo costo
                nodo_actual = i
                min = costo_minimo[i]
    camino = ""
    for n in range(len(mAd)):
        camino += str(nodo_actual+1)  #Crear un nuevo formato para la visualizacion del código
        if nodo_actual == inicio:
            break
        nodo_actual = recorrido_minimo[nodo_actual]
        camino += ","
    camino = camino[::-1]
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
    # Bucle con limite que recorrera los nodos hasta que no exista nodo actual
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
        # Bucle que busca un nuevo nodo actual segun el minimo camino disponible
        # si no existe un minimo de algun nodo no visitado, el nodo actual no tendria valor y el proceso se detiene
        for nodo in costo_minimo:
            if nodo not in nodos_visitados:
                min = costo_minimo[nodo] if min is None else min
                if costo_minimo[nodo] <= min:  # Elegir un nuevo nodo a evaluar segun el minimo costo
                    min = costo_minimo[nodo]
                    nodo_actual = nodo
    camino = []
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = recorrido_de_nodos[nodo_actual]
    return camino[::-1]

def Dijkstra_v3(costo_minimo, recorrido_de_nodos, nodos_visitados, nodo_actual, grafo):
    """Tercera version de algoritmo basado en la version 2. Preparado para ejecutarse
    una sola vez y devolver la informacion actualizada de las variables necesarias para realizar la busqueda. Util para
    ser llamado en ejecuciones donde se requiere tener la informacion del avance del proceso de busqueda nodo por nodo."""
    # Proceso
    # Bucle con limite que recorrera los nodos hasta que no exista nodo actual
    if nodo_actual is not None:
        nodos_visitados.append(nodo_actual)
        for nodo_vecino in grafo[nodo_actual]:
            punto_vecino, costo_de_vecino = nodo_vecino
            if punto_vecino not in costo_minimo or costo_minimo[nodo_actual] + costo_de_vecino < costo_minimo[punto_vecino]:
                costo_minimo[punto_vecino] = costo_minimo[nodo_actual] + costo_de_vecino
                recorrido_de_nodos[punto_vecino] = nodo_actual
        min = None
        nodo_actual = None
        # Bucle que busca un nuevo nodo actual segun el minimo camino disponible
        # si no existe un minimo de algun nodo no visitado, el nodo actual no tendria valor y el proceso se detiene
        for nodo in costo_minimo:
            if nodo not in nodos_visitados:
                min = costo_minimo[nodo] if min is None else min
                if costo_minimo[nodo] <= min:  # Elegir un nuevo nodo a evaluar segun el minimo costo
                    min = costo_minimo[nodo]
                    nodo_actual = nodo
    camino, nodo_de_camino = [], nodo_actual
    while nodo_de_camino is not None:
        camino.append(nodo_de_camino)
        nodo_de_camino = recorrido_de_nodos[nodo_de_camino]
    return costo_minimo, recorrido_de_nodos, nodos_visitados, nodo_actual, camino[::-1]