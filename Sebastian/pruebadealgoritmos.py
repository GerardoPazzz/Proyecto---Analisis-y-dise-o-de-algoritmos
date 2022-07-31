from CaminosMinimos import *
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
               [max_Int,max_Int,max_Int,6,2,max_Int]]
grid=[[0,0,0],
      [0,5,0],
      [0,0,0]]
print(Dijkstra_v2((0,0),(2,2),convertir_grid(grid)))

