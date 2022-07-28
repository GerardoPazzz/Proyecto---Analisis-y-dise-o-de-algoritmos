from CaminosMinimos import *
matrizPrueba=[[0,4,8,max_Int,max_Int],
              [4,0,1,2,max_Int],
              [8,1,0,4,2],
              [max_Int,2,4,0,7],
              [max_Int,max_Int,2,7,0]]
print(Dijkstra(0,4,matrizPrueba))
