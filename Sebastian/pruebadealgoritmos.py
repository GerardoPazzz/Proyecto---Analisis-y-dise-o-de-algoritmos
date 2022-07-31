import time
from CaminosMinimos import *
# Declaracion de matrices para pruebas
"""
matrizPrueba=[[0,4,8,max_Int,max_Int],
              [4,0,1,2,max_Int],
              [8,1,0,4,2],
              [max_Int,2,4,0,7],
              [max_Int,max_Int,2,7,0]]
matrizPrueba2=[[max_Int,4,2,max_Int,max_Int,max_Int],
               [4,max_Int,1,5,max_Int,max_Int],
               [2,1,max_Int,8,10,max_Int],
               [max_Int,5,8,max_Int,2,6],
               [max_Int,max_Int,10,2,max_Int,2],
               [max_Int,max_Int,max_Int,6,2,max_Int]]"""
# 1 -> vacio, 2 -> camino, 3 -> cesped, 4 -> agua, 5 -> bosque, 6 -> pared
grid = [[3,3,3,3,3,3,3],
       [3,3,6,6,6,6,3],
       [3,6,3,6,3,3,3],
       [3,3,3,6,3,6,3],
       [3,6,3,3,3,3,3]]
# Variables de algoritmo
grafo = convertir_grid(grid)
inicio, final = ((0, 0), (4, 2))
costo_minimo = {inicio: 0}
recorrido_de_nodos = {inicio: None}
nodos_visitados = []
nodo_actual = inicio
camino=[]
# Bucle de algoritmo y graficos en consola
while True:
    limpiar_consola()
    if nodo_actual != final:
        costo_minimo,recorrido_de_nodos,nodos_visitados,nodo_actual,camino=\
            Dijkstra_v3(costo_minimo,recorrido_de_nodos,nodos_visitados,nodo_actual,grafo)
    #print(camino)
    pintar_grafo_en_consola([[(grid[fil][col]," I " if (col,fil) == inicio else " F " if (col,fil) == final else
    " C " if (col,fil) in camino else " V " if (col,fil) in nodos_visitados else "   ")
    for col in range(len(grid[fil]))]for fil in range(len(grid))])
    time.sleep(0.5)