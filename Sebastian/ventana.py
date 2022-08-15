import time
import tkinter    #Libreria para ventanas
from tkinter import  messagebox, ttk
from CaminosMinimos import  *

ventana = tkinter.Tk()
#ventana.geometry("800x600")
#etiqueta=tkinter.Label(ventana,text="PROYECTO DE CURSO")
#etiqueta.pack(side=tkinter.BOTTOM) # -> decirle que aparezca en pantalla
#boton1=tkinter.Button(ventana,text="Guarda",padx=50,pady=25,command=suma)
#boton1.pack(side=tkinter.RIGHT)
#txtfield=tkinter.Entry(ventana,font="Arial 20")
#txtfield.pack()

flag_buscando=False
flag_pausado=False
flag_reiniciado=False

#Configuraciones del editor de mapa (Grafo)
GRID_ALTO=23
GRID_ANCHO=23
TAMAÑO_DE_SPRITE=16
BORDE_DE_GRID=1
tile_cesped = tkinter.PhotoImage(file="imagenes/cesped.png")
tile_basico_pared = tkinter.PhotoImage(file="imagenes/basico_pared.png")
tile_basico_suelo = tkinter.PhotoImage(file="imagenes/basico_suelo.png")
nodo_tile_actual=tile_basico_pared
peso_nodo_actual=1

#CODIGO PARA DIJKSTRA
grid = [[peso_nodo_actual for i in range(GRID_ANCHO)]for j in range(GRID_ALTO)]
inicio, final = ((0, 0), (GRID_ANCHO-1, GRID_ALTO-1))  # Configuracion del punto de inicio y final
lista_graficos_nodos=[]
#Funciones
def pintar_tile_en_canvas(x,y,tile):
    canvas_grafo.create_image(x,y,image=tile,anchor=tkinter.NW,tag="tile")
    pass
def repintar_tile(event):
    if not flag_buscando:
        global peso_nodo_actual
        peso_nodo_actual="Inf"
        item_nodo=canvas_grafo.find_closest(event.x,event.y)
        nodo_actual_x, nodo_actual_y = canvas_grafo.coords(item_nodo)
        #pintar_tile_en_canvas(nodo_actual_x,nodo_actual_y,nodo_tile_actual) # -> Opcion demandante
        canvas_grafo.itemconfig(item_nodo, image=tile_basico_pared)  # -> Opcion optimizada
        grid[int(nodo_actual_y/(TAMAÑO_DE_SPRITE+BORDE_DE_GRID))][int(nodo_actual_x/(TAMAÑO_DE_SPRITE+BORDE_DE_GRID))]=peso_nodo_actual
    #print(grid)
    pass

def despintar_tile(event):  # Opcion temporal para mejorar el control sobre el modo pintar
    if not flag_buscando:
        global peso_nodo_actual
        peso_nodo_actual=1
        item_nodo=canvas_grafo.find_closest(event.x,event.y)
        nodo_actual_x, nodo_actual_y = canvas_grafo.coords(item_nodo)
        #pintar_tile_en_canvas(nodo_actual_x,nodo_actual_y,nodo_tile_actual) # -> Opcion demandante
        canvas_grafo.itemconfig(item_nodo, image=tile_basico_suelo)  # -> Opcion optimizada
        grid[int(nodo_actual_y/(TAMAÑO_DE_SPRITE+BORDE_DE_GRID))][int(nodo_actual_x/(TAMAÑO_DE_SPRITE+BORDE_DE_GRID))]=peso_nodo_actual
    #print(grid)
    pass

def borrar_grafo():
    canvas_grafo.itemconfig("tile", image=tile_basico_suelo)
    for j in range(GRID_ALTO):
        for i in range(GRID_ANCHO):
            grid[j][i]=1

def iniciar_busqueda():
    boton_iniciar_busqueda.config(bg="red",text="PAUSAR",command=pausar)
    global flag_buscando
    global flag_reiniciado
    global flag_pausado
    flag_buscando=True
    tiempo=time.time()*1000
    grafo = convertir_grid(grid)
    costo_minimo = {inicio: 0}
    recorrido_de_nodos = {inicio: None}
    nodos_visitados = []
    nodo_actual = inicio
    camino = []
    # Variables para graficos
    global lista_graficos_nodos # Para manejar graficos al dibujar el proceso en el canvas, necesario para mejor rendimiento
    while nodo_actual != final and not flag_reiniciado:
        if not flag_pausado:
            costo_minimo, recorrido_de_nodos, nodos_visitados, nodo_actual, camino = \
                Dijkstra_v3(costo_minimo, recorrido_de_nodos, nodos_visitados, nodo_actual, grafo)
            if nodo_actual is None:
                messagebox.showinfo(title="Camino no existente",
                                    message="No existe camino para llegar al punto final")
                flag_reiniciado=True
                break
            label_nodo_evaluado.config(text=f"({nodo_actual[0]},{nodo_actual[1]})")
            label_nodos_visitados.config(text=f"{len(nodos_visitados)}")
            label_nodos_camino.config(text=f"{len(camino)}")
            while len(lista_graficos_nodos) < len(camino):
                lista_graficos_nodos.append(canvas_grafo.create_oval(0,0,TAMAÑO_DE_SPRITE,TAMAÑO_DE_SPRITE, fill="blue",tags="nodo_camino"))
            canvas_grafo.itemconfig("nodo_camino",state="hidden")
            indice_lista_graficos=0
            for j in range(GRID_ALTO):
                for i in range(GRID_ANCHO):
                    if (i,j) != inicio and (i,j) != final and (i,j) in camino:
                        canvas_grafo.itemconfig(lista_graficos_nodos[indice_lista_graficos], state="normal")
                        canvas_grafo.moveto(lista_graficos_nodos[indice_lista_graficos],
                                            i*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,j*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID)
                        indice_lista_graficos+=1
            #print(camino)
            #time.sleep(0.1)
        ventana.update()
    if flag_reiniciado:
        canvas_grafo.itemconfig("nodo_camino",state="hidden")
        #canvas_grafo.delete("nodo_camino")
        #lista_graficos_nodos.clear()
    flag_reiniciado=False
    flag_buscando=False
    flag_pausado=False
    label_ultima_evaluacion.config(text=f"{time.time()*1000-tiempo:.0f}")
    boton_iniciar_busqueda.config(bg="green", text="INICIAR\nBÚSQUEDA",command=iniciar_busqueda)
    pass
def reiniciar():
    if not flag_buscando:
        canvas_grafo.itemconfig("nodo_camino",state="hidden")
        #canvas_grafo.delete("nodo_camino")
        #lista_graficos_nodos.clear()
    else:
        global flag_reiniciado
        flag_reiniciado=True

def pausar():
    boton_iniciar_busqueda.config(bg="blue",text="CONTINUAR\nBÚSQUEDA",command=quitar_pausa,fg="white")
    global flag_pausado
    flag_pausado = True
def quitar_pausa():
    boton_iniciar_busqueda.config(bg="red", text="PAUSAR", command=pausar)
    global flag_pausado
    flag_pausado = False

# Funciones para obtener datos
def obtener_punto_inicial(*args):
    global inicio
    punto=text_punto_inicial.get().strip()
    try:
        entry_punto_inicial.config(highlightbackground="white", highlightcolor="white")
        x,y=punto.split(",")
        if x.startswith("("):
            x=x[1:len(x)]
        x=x.strip()
        if y.endswith(")"):
            y=y[0:len(y)-1]
        y=y.strip()
        if x.isdigit() and y.isdigit():
            if 0<=int(x)<GRID_ANCHO and 0<=int(y)<GRID_ALTO:
                punto_lst=list(inicio)
                punto_lst[0],punto_lst[1]=int(x),int(y)
                inicio=tuple(punto_lst)
                canvas_grafo.moveto(grafico_nodo_inicio,inicio[0]*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,
                                    inicio[1]*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID)
            else:
                raise Exception("Valores fuera del limite")
        else:
            raise Exception("Valores ingresados no son numeros")
    except:
        entry_punto_inicial.config(highlightbackground="red",highlightcolor="red")

def obtener_punto_final(*args):
    global final
    punto=text_punto_final.get().strip()
    try:
        entry_punto_final.config(highlightbackground="white", highlightcolor="white")
        x,y=punto.split(",")
        if x.startswith("("):
            x=x[1:len(x)]
        x=x.strip()
        if y.endswith(")"):
            y=y[0:len(y)-1]
        y=y.strip()
        if x.isdigit() and y.isdigit():
            if 0<=int(x)<GRID_ANCHO and 0<=int(y)<GRID_ALTO:
                punto_lst=list(final)
                punto_lst[0],punto_lst[1]=int(x),int(y)
                final=tuple(punto_lst)
                canvas_grafo.moveto(grafico_nodo_final, final[0]*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,
                                    final[1]*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID)
            else:
                raise Exception("Valores fuera del limite")
        else:
            raise Exception("Valores ingresados no son numeros")
    except:
        entry_punto_final.config(highlightbackground="red",highlightcolor="red")

def cambiar_tamaño_canvas_grafo(alto,ancho):
    canvas_grafo.config(width=ancho*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,height=alto*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,bg="gray")
    nuevo_grid=[]
    global grid
    global GRID_ALTO
    global GRID_ANCHO
    for j in range(alto):
        fila=[]
        for i in range(ancho):
            fila.append(grid[j][i])
        nuevo_grid.append(fila)
    grid=nuevo_grid
    GRID_ALTO=alto
    GRID_ANCHO=ancho
    contenedor_grafo.update()
    #print(contenedor_grafo.winfo_width()/2,contenedor_grafo.winfo_height()/2)
    canvas_grafo.place(x=contenedor_grafo.winfo_width()/2, y=contenedor_grafo.winfo_height()/2,anchor="center")

def obtener_tamaño_grafo(*args):
    global GRID_ANCHO
    global GRID_ALTO
    global final
    contenedor_grafo.update()
    tamaño = entry_tamaño_grafo.get()
    try:
        entry_tamaño_grafo.config(highlightbackground="white", highlightcolor="white")
        ancho, alto = tamaño.split("x")
        ancho = ancho.strip()
        alto = alto.strip()
        if ancho.isdigit() and alto.isdigit():
            if 0 < int(ancho) and 0 < int(alto):
                if int(ancho)*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)<contenedor_grafo.winfo_width() and \
                    int(alto)*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)<contenedor_grafo.winfo_height():
                    cambiar_tamaño_canvas_grafo(int(alto),int(ancho))
                    """canvas_grafo.moveto(grafico_nodo_final,
                                        (ancho-1) * (TAMAÑO_DE_SPRITE + BORDE_DE_GRID) + BORDE_DE_GRID,
                                        (alto-1) * (TAMAÑO_DE_SPRITE + BORDE_DE_GRID) + BORDE_DE_GRID)
                    punto_lst = list(final)
                    punto_lst[0], punto_lst[1] = int(ancho-1), int(alto-1)
                    final = tuple(punto_lst)
                    entry_punto_final.delete(0,tkinter.END)
                    entry_punto_final.insert(tkinter.END,f"({final[0]}x{final[1]})")"""
                else:
                    raise Exception("Valores fuera del limite del contenedor de grafo")
            else:
                raise Exception("Valores no aceptados para grafo")
        else:
            raise Exception("Valores ingresados no son numeros")
    except(Exception):
        print(Exception)
        entry_tamaño_grafo.config(highlightbackground="red", highlightcolor="red")



# CODIGO PARA VENTANA
GRIS_OSCURO = "#1F2022"  # color del fondo en hexadecimal
fuente_titulo=("Arial",9)  #Fuente para titulo de frame de grafo
fuente_opciones=("Arial",8) #Fuente para opciones de frame de grafo
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
#framenodos.pack(side=tkinter.LEFT, padx=10, pady=10)
# FRAME DE GRAFO
framegrafo = tkinter.Frame(fondo, bg=GRIS_OSCURO,highlightbackground="gray", highlightthickness=1)
framegrafo.config(width=460, height=560)
# framegrafo.grid(row=0,column=1,padx=10,pady=10)
framegrafo.pack(side=tkinter.BOTTOM, padx=(10, 10), pady=10)

# Elementos de frame de grafo
# Frame de grafo (Panel que pondra limites al grafo)
contenedor_grafo=tkinter.Frame(framegrafo,bg=GRIS_OSCURO, highlightbackground="gray", highlightthickness=1,height=416)
contenedor_grafo.pack_propagate(False)
contenedor_grafo.pack(side=tkinter.TOP, padx=5, pady=(5,0),fill=tkinter.BOTH)
# Canvas de grafo (Donde se dibujara el grafo)
canvas_grafo = tkinter.Canvas(contenedor_grafo, highlightthickness=0)
#canvas_grafo.config(width=0, height=0)
#canvas_grafo.pack_propagate(False)
canvas_grafo.pack()
# Frame de configuracion de grafo
configuracion_de_grafo = tkinter.Frame(framegrafo, bg=GRIS_OSCURO,highlightbackground="gray", highlightthickness=1)
configuracion_de_grafo.config(width=150, height=120)
configuracion_de_grafo.pack(side=tkinter.LEFT, padx=(5, 5), pady=5,fill=tkinter.Y)
#Variables de control
text_punto_inicial=tkinter.StringVar()
text_punto_inicial.set(f"({inicio[0]},{inicio[1]})")
text_punto_inicial.trace("w",obtener_punto_inicial)
text_punto_final=tkinter.StringVar()
text_punto_final.set(f"({final[0]},{final[1]})")
text_punto_final.trace("w",obtener_punto_final)
#Labels y Entrys
tkinter.Label(configuracion_de_grafo,text="CONFIGURACIÓN DE GRAFO",fg="white",bg=GRIS_OSCURO,font=fuente_titulo).grid(row=0,columnspan=2)
tkinter.Label(configuracion_de_grafo,text="Punto inicial:",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=1,column=0,sticky="e")
entry_punto_inicial = tkinter.Entry(configuracion_de_grafo,width=8,textvariable=text_punto_inicial,bd=0,highlightbackground="white",highlightcolor="white",highlightthickness=1)
entry_punto_inicial.grid(row=1,column=1,sticky="w")
tkinter.Label(configuracion_de_grafo,text="Punto final:",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=2,column=0,sticky="e")
entry_punto_final = tkinter.Entry(configuracion_de_grafo,width=8,textvariable=text_punto_final,bd=0,highlightbackground="white",highlightcolor="white",highlightthickness=1)
entry_punto_final.grid(row=2,column=1,sticky="w")
ttk.Separator(configuracion_de_grafo,orient='horizontal').grid(row=3,columnspan=2,ipadx=75,ipady=0,pady=3)
tkinter.Label(configuracion_de_grafo,text="Ancho x Alto:",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=4,column=0,sticky="e")
entry_tamaño_grafo = tkinter.Entry(configuracion_de_grafo,width=8,bd=0,highlightbackground="white",highlightcolor="white",highlightthickness=1)
entry_tamaño_grafo.insert(tkinter.END,f"{GRID_ANCHO}x{GRID_ALTO}")
entry_tamaño_grafo.grid(row=4,column=1,sticky="w")
tkinter.Label(configuracion_de_grafo,text="Tamaño de imagen:",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=5,column=0,sticky="e")
label_tamaño_imagen = tkinter.Label(configuracion_de_grafo,text="16 px",fg="white",bg=GRIS_OSCURO,font=fuente_opciones)
label_tamaño_imagen.grid(row=5,column=1,sticky="w")
tkinter.Label(configuracion_de_grafo,text="Mostrar rejilla",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=6,column=0,sticky="e")
boton_aceptar_cambios = tkinter.Button(configuracion_de_grafo, text="Aceptar", bg="gray",command=obtener_tamaño_grafo)
boton_aceptar_cambios.grid(row=7,column=0,sticky="we")
boton_borrar_grafo = tkinter.Button(configuracion_de_grafo, text="Borrar grafo", bg="gray",command=borrar_grafo)
boton_borrar_grafo.grid(row=7,column=1)
# Frame de configuracion de busqueda
configuracion_de_busqueda = tkinter.Frame(framegrafo, bg=GRIS_OSCURO,highlightbackground="gray", highlightthickness=1)
configuracion_de_busqueda.config(width=150, height=120)
configuracion_de_busqueda.pack(side=tkinter.LEFT, padx=(0, 5), pady=5,fill=tkinter.Y)

tkinter.Label(configuracion_de_busqueda,text="            CONFIGURACIÓN DE BÚSQUEDA            ",fg="white",bg=GRIS_OSCURO,font=fuente_titulo).grid(row=0,columnspan=2)
tkinter.Label(configuracion_de_busqueda,text="Nodo evaluado:",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=1,column=0,sticky="e")
label_nodo_evaluado=tkinter.Label(configuracion_de_busqueda,text="(0,0)",fg="white",bg=GRIS_OSCURO,font=fuente_opciones)
label_nodo_evaluado.grid(row=1,column=1,sticky="w")
tkinter.Label(configuracion_de_busqueda,text="Tiempo de retraso(ms):",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=2,column=0,sticky="e")
tkinter.Entry(configuracion_de_busqueda,width=8).grid(row=2,column=1,sticky="w")
tkinter.Label(configuracion_de_busqueda,text="Número de nodos visitados:",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=3,column=0,sticky="e")
label_nodos_visitados=tkinter.Label(configuracion_de_busqueda,text="0",fg="white",bg=GRIS_OSCURO,font=fuente_opciones)
label_nodos_visitados.grid(row=3,column=1,sticky="w")
tkinter.Label(configuracion_de_busqueda,text="Número de nodos de camino mínimo:",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=4,column=0,sticky="e")
label_nodos_camino=tkinter.Label(configuracion_de_busqueda,text="0",fg="white",bg=GRIS_OSCURO,font=fuente_opciones)
label_nodos_camino.grid(row=4,column=1,sticky="w")
tkinter.Label(configuracion_de_busqueda,text="Último tiempo de evaluación(ms):",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=5,column=0,sticky="e")
label_ultima_evaluacion=tkinter.Label(configuracion_de_busqueda,text="0",fg="white",bg=GRIS_OSCURO,font=fuente_opciones)
label_ultima_evaluacion.grid(row=5,column=1,sticky="w")
tkinter.Label(configuracion_de_busqueda,text="Mostrar camino mínimo",fg="white",bg=GRIS_OSCURO,font=fuente_opciones).grid(row=6,column=0,sticky="e")

# Boton de reiniciar
boton_reiniciar = tkinter.Button(framegrafo, text="REINICIAR", bg="yellow",command=reiniciar)
boton_reiniciar.config(width=14, height=4)
boton_reiniciar.pack(side=tkinter.TOP, padx=(0, 3), pady=5)
# Boton de iniciar busqueda
boton_iniciar_busqueda = tkinter.Button(framegrafo, text="INICIAR\nBÚSQUEDA", bg="green",command=iniciar_busqueda)
boton_iniciar_busqueda.config(width=14, height=4)
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
cambiar_tamaño_canvas_grafo(GRID_ALTO,GRID_ANCHO)
for j in range(GRID_ALTO):
    for i in range(GRID_ANCHO):
        sprite=canvas_grafo.create_image(i*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,
                                         j*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,
        image=tile_basico_suelo,anchor=tkinter.NW,tags="tile")
canvas_grafo.tag_bind("tile", "<1>", repintar_tile)
canvas_grafo.tag_bind("tile","<B1-Motion>",repintar_tile)
canvas_grafo.tag_bind("tile", "<3>", despintar_tile)
canvas_grafo.tag_bind("tile","<B3-Motion>",despintar_tile)
# Creacion de los graficos de los puntos de inicio y final
grafico_nodo_inicio = canvas_grafo.create_oval(1,1,TAMAÑO_DE_SPRITE-1,TAMAÑO_DE_SPRITE-1,fill="red",width=0)
canvas_grafo.moveto(grafico_nodo_inicio,inicio[0]*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,
                    inicio[1]*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID)
grafico_nodo_final = canvas_grafo.create_oval(1,1,TAMAÑO_DE_SPRITE,TAMAÑO_DE_SPRITE,fill="yellow",width=0)
canvas_grafo.moveto(grafico_nodo_final,final[0]*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID,
                    final[1]*(TAMAÑO_DE_SPRITE+BORDE_DE_GRID)+BORDE_DE_GRID)

ventana.mainloop()
