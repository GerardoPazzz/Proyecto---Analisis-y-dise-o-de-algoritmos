#Constantes
"""Valor 'Infinito'"""
max_Int=2**63-1
#Definicion de Funciones
"""Primera version de algoritmo que utiliza una matriz de adyacencia y un valor maximo para obtener el camino minimo"""
def Dijkstra(inicio,final,mAd):
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
