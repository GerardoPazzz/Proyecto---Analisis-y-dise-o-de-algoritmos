import tkinter

ventana = tkinter.Tk()
#ventana.geometry("800x600")
#etiqueta=tkinter.Label(ventana,text="PROYECTO DE CURSO")
#etiqueta.pack(side=tkinter.BOTTOM) # -> decirle que aparezca en pantalla
#boton1=tkinter.Button(ventana,text="Guarda",padx=50,pady=25,command=suma)
#boton1.pack(side=tkinter.RIGHT)
#txtfield=tkinter.Entry(ventana,font="Arial 20")
#txtfield.pack()

#Configuraciones del editor de mapa (Grafo)
GRID_ALTO=26
GRID_ANCHO=26
TAMAÑO_DE_SPRITE=16
tile_cesped = tkinter.PhotoImage(file="imagenes/cesped.png")
tile_basico_pared = tkinter.PhotoImage(file="imagenes/basico_pared.png")
tile_basico_suelo = tkinter.PhotoImage(file="imagenes/basico_suelo.png")
nodo_tile_actual=tile_basico_pared
peso_nodo_actual=1

#CODIGO PARA DIJKSTRA
grid = [[peso_nodo_actual for i in range(GRID_ANCHO)]for j in range(GRID_ALTO)]

#Funciones
def pintar_tile_en_canvas(x,y,tile):
    canvas_grafo.create_image(x,y,image=tile,anchor=tkinter.NW,tag="tile")
    pass
def repintar_tile(event):
    global peso_nodo_actual
    peso_nodo_actual=5
    nodo_actual_x, nodo_actual_y = canvas_grafo.coords(canvas_grafo.find_closest(event.x,event.y))
    pintar_tile_en_canvas(nodo_actual_x,nodo_actual_y,nodo_tile_actual)
    grid[int(nodo_actual_y/16)][int(nodo_actual_x/16)]=peso_nodo_actual
    print(grid)
    pass
# CODIGO PARA VENTANA
GRIS_OSCURO = "#1F2022"  # color del fondo en hexadecimal
ventana.title("Proyecto Dijkstra")
# Frame de fondo (PRINCIPAL)
fondo = tkinter.Frame()
fondo.config(width=800, height=600, bg=GRIS_OSCURO)
fondo.pack()
# Elementos de frame de fondo
# FRAME DE NODOS
framenodos = tkinter.Frame(fondo, bg=GRIS_OSCURO, highlightbackground="gray", highlightthickness=1)
framenodos.config(width=300, height=570)
# framenodos.grid(row=0,column=0,padx=10,pady =10)
framenodos.pack(side=tkinter.LEFT, padx=10, pady=10)
# FRAME DE GRAFO
framegrafo = tkinter.Frame(fondo, bg=GRIS_OSCURO,highlightbackground="gray", highlightthickness=1)
framegrafo.config(width=460, height=560)
# framegrafo.grid(row=0,column=1,padx=10,pady=10)
framegrafo.pack(side=tkinter.BOTTOM, padx=(0, 10), pady=10)

# Elementos de frame de grafo
# Frame de grafo (donde se mostrara el mapa)
canvas_grafo = tkinter.Canvas(framegrafo, highlightbackground="gray", highlightthickness=1)
canvas_grafo.config(width=416, height=416)
canvas_grafo.pack(side=tkinter.TOP, padx=(5, 5), pady=(5, 0))
# Frame de configuracion de grafo
configuracion_de_grafo = tkinter.Frame(framegrafo, bg=GRIS_OSCURO,highlightbackground="gray", highlightthickness=1)
configuracion_de_grafo.config(width=150, height=120)
configuracion_de_grafo.pack(side=tkinter.LEFT, padx=(5, 5), pady=5)
# Frame de configuracion de busqueda
configuracion_de_busqueda = tkinter.Frame(framegrafo, bg=GRIS_OSCURO,highlightbackground="gray", highlightthickness=1)
configuracion_de_busqueda.config(width=150, height=120)
configuracion_de_busqueda.pack(side=tkinter.LEFT, padx=(0, 5), pady=5)
# Boton de reiniciar
boton_reiniciar = tkinter.Button(framegrafo, text="REINICIAR", bg="yellow")
boton_reiniciar.config(width=14, height=3)
boton_reiniciar.pack(side=tkinter.TOP, padx=(0, 3), pady=5)
# Boton de iniciar busqueda
boton_iniciar_busqueda = tkinter.Button(framegrafo, text="INICIAR \nBUSQUEDA", bg="green")
boton_iniciar_busqueda.config(width=14, height=3)
boton_iniciar_busqueda.pack(side=tkinter.BOTTOM, padx=(0, 3), pady=(0, 5))

# Elementos de frame de nodos
editor_de_nodos = tkinter.Frame(framenodos, bg=GRIS_OSCURO, highlightbackground="gray", highlightthickness=1)
editor_de_nodos.config(width=256, height=256)
editor_de_nodos.pack(side=tkinter.BOTTOM, padx=5, pady=5)
lista_de_nodos = tkinter.Frame(framenodos, bg=GRIS_OSCURO, highlightbackground="gray", highlightthickness=1)
lista_de_nodos.config(width=256, height=216)
lista_de_nodos.pack(side=tkinter.LEFT, padx=5, pady=(5, 0))


# Prueba de creacion de grid con imagenes
#sprite=Image.open("imagenes/cesped.png")
#Crear grid en ventana
for j in range(GRID_ALTO):
    for i in range(GRID_ANCHO):
        sprite=canvas_grafo.create_image(i*TAMAÑO_DE_SPRITE,j*TAMAÑO_DE_SPRITE,image=tile_basico_suelo,anchor=tkinter.NW,tags="tile")
canvas_grafo.tag_bind("tile", "<1>", repintar_tile)
canvas_grafo.tag_bind("tile","<B1-Motion>",repintar_tile)
ventana.mainloop()
