"""
import tkinter as ventana  # uso de la libreria tkinter que permite crear la interfaz gráfica de la app, 

ventana_main = ventana.Tk() # ventana principal del app
ventana_main.title("APP") # nombre de la ventana

# Para obtener el tamaño de la pantalla del usuario, así lo podemos centrar la ventana adaptando a cualquier usuario
screen_width = ventana_main.winfo_screenwidth()
screen_height = ventana_main.winfo_screenheight()

# Tamaño de la ventana, se ha puesto 1070 x 600 (ventana ancha simulando a IPAD)
ancho = 600
alto = 900

# Calcular posición centrada
pos_x = (screen_width - ancho) // 2
pos_y = (screen_height - alto) // 2

# Aplicamos los tamaños a la ventana_principal: EJ: "1070x600+425+200", donde 1070 es el ancho, 600 altura
# 425 distancia desde el borde izquierdo de la pantalla, y 200 distancia desde el borde superior.
# ancho x altura + distancia desde borde izq + distancia desde borde der 

ventana_main.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


# Aquí metemos la estaciones del METRO MÉXICO
estaciones = [
    "Madrid Atocha",
    "Madrid Chamartín",
    "Barcelona Sants",
    "Valencia Nord",
    "Sevilla Santa Justa",
    "Bilbao Abando",
    "Málaga María Zambrano",
    "Zaragoza Delicias",
    "Toledo",
    "Córdoba Central",
    "Granada",
    "Alicante Terminal"
]

# centrado de todo
centro_x = (ancho - 300) // 2   # 300 es el ancho del botón/lista
boton_y = 70                    # altura donde poner el botón
lista_y = boton_y + 50         # lista justo debajo

lista_visible = False

def toggle_lista():
    global lista_visible
    if lista_visible:
        listbox_estaciones.place_forget()  # ocultar
        lista_visible = False
    else:
        listbox_estaciones.place(x=centro_x, y=lista_y, width=300)
        lista_visible = True


boton_estaciones = ventana.Button(
    ventana_main,
    text="Seleccionar estación ▼",
    font=("Arial", 14),
    command=toggle_lista
)
boton_estaciones.place(x=centro_x, y=boton_y, width=300)

listbox_estaciones = ventana.Listbox(ventana_main, font=("Arial", 14), height=8)

for est in estaciones:
    listbox_estaciones.insert(ventana.END, est)


# mainloop mantiene la ventana abierta
ventana_main.mainloop()



"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import networkx as nx
import math
import heapq

# ========================== #
# 1. CONFIGURACIÓN DEL GRAFO #
# ========================== #

def crear_grafo_metro():
    metro = nx.Graph()
    
    # Coordenadas aproximadas basadas en la imagen "Mapa_metro.jpg"
    # Suponiendo que la imagen se redimensiona a unos 700x750 px en la app.
    
    # --- EJES PRINCIPALES (Referencias visuales) ---
    X_L7 = 180        # Eje vertical izquierdo (Línea Naranja)
    X_L3 = 600        # Eje vertical derecho (Línea Verde Oliva)
    Y_L9 = 320        # Eje horizontal medio (Línea Marrón) - Tacubaya a Centro Medico
    Y_L12 = 550       # Eje horizontal inferior (Línea Dorada) - Mixcoac a Zapata
    
    # ----------------------------------------------------------
    # LÍNEA 7 (Naranja) - Vertical Izquierda
    # ----------------------------------------------------------
    metro.add_node("Polanco_L7",              pos=(X_L7, 50),  linea="L7", nombre="Polanco")
    metro.add_node("Auditorio_L7",            pos=(X_L7, 120), linea="L7", nombre="Auditorio")
    metro.add_node("Constituyentes_L7",       pos=(X_L7, 200), linea="L7", nombre="Constituyentes")
    metro.add_node("Tacubaya_L7",             pos=(X_L7, Y_L9), linea="L7", nombre="Tacubaya") # HUB
    metro.add_node("San Pedro de los Pinos_L7", pos=(X_L7, 400), linea="L7", nombre="San Pedro de los Pinos")
    metro.add_node("San Antonio_L7",          pos=(X_L7, 470), linea="L7", nombre="San Antonio")
    metro.add_node("Mixcoac_L7",              pos=(X_L7, Y_L12), linea="L7", nombre="Mixcoac") # HUB
    metro.add_node("Barranca del Muerto_L7",  pos=(X_L7, 630), linea="L7", nombre="Barranca del Muerto")

    # ----------------------------------------------------------
    # LÍNEA 3 (Verde Oliva) - Vertical Derecha
    # ----------------------------------------------------------
    metro.add_node("Juarez_L3",              pos=(X_L3, 50),  linea="L3", nombre="Juarez")
    metro.add_node("Balderas_L3",            pos=(X_L3, 110), linea="L3", nombre="Balderas") # HUB
    metro.add_node("Ninos Heroes_L3",        pos=(X_L3, 180), linea="L3", nombre="Niños Heroes")
    metro.add_node("Hospital General_L3",    pos=(X_L3, 250), linea="L3", nombre="Hospital General")
    metro.add_node("Centro Medico_L3",       pos=(X_L3, Y_L9), linea="L3", nombre="Centro Medico") # HUB
    metro.add_node("Etiopia_L3",             pos=(X_L3, 380), linea="L3", nombre="Etiopia")
    metro.add_node("Eugenia_L3",             pos=(X_L3, 440), linea="L3", nombre="Eugenia")
    metro.add_node("Division del Norte_L3",  pos=(X_L3, 500), linea="L3", nombre="Division del Norte")
    metro.add_node("Zapata_L3",              pos=(X_L3, Y_L12), linea="L3", nombre="Zapata") # HUB
    metro.add_node("Coyoacan_L3",            pos=(X_L3, 600), linea="L3", nombre="Coyoacan")
    metro.add_node("Viveros_L3",             pos=(X_L3, 650), linea="L3", nombre="Viveros")
    metro.add_node("M.A. de Quevedo_L3",     pos=(X_L3, 700), linea="L3", nombre="M.A. de Quevedo")
    metro.add_node("Copilco_L3",             pos=(X_L3, 740), linea="L3", nombre="Copilco")
    metro.add_node("Universidad_L3",         pos=(X_L3, 780), linea="L3", nombre="Universidad")

    # ----------------------------------------------------------
    # LÍNEA 9 (Marrón) - Horizontal Media
    # ----------------------------------------------------------
    metro.add_node("Tacubaya_L9",        pos=(X_L7, Y_L9), linea="L9", nombre="Tacubaya") # HUB
    metro.add_node("Patriotismo_L9",     pos=(320, Y_L9), linea="L9", nombre="Patriotismo")
    metro.add_node("Chilpancingo_L9",    pos=(460, Y_L9), linea="L9", nombre="Chilpancingo")
    metro.add_node("Centro Medico_L9",   pos=(X_L3, Y_L9), linea="L9", nombre="Centro Medico") # HUB
    metro.add_node("Lazaro Cardenas_L9", pos=(700, Y_L9), linea="L9", nombre="Lazaro Cardenas")

    # ----------------------------------------------------------
    # LÍNEA 12 (Dorada) - Horizontal Inferior
    # ----------------------------------------------------------
    metro.add_node("Mixcoac_L12",           pos=(X_L7, Y_L12), linea="L12", nombre="Mixcoac") # HUB
    metro.add_node("Insurgentes Sur_L12",   pos=(320, Y_L12), linea="L12", nombre="Insurgentes Sur")
    metro.add_node("Hospital 20 de Nov_L12",pos=(460, Y_L12), linea="L12", nombre="Hospital 20 de Nov")
    metro.add_node("Zapata_L12",            pos=(X_L3, Y_L12), linea="L12", nombre="Zapata") # HUB
    # Ojo: En el mapa L12 baja hacia la derecha después de Zapata
    metro.add_node("Parque de los Venados_L12", pos=(700, Y_L12), linea="L12", nombre="Parque de los Venados")
    metro.add_node("Eje Central_L12",       pos=(740, 620), linea="L12", nombre="Eje Central") # Baja visualmente

    # ----------------------------------------------------------
    # LÍNEA 1 (Rosa) - Diagonal / Horizontal Superior
    # ----------------------------------------------------------
    # Observatorio está abajo a la izquierda de Tacubaya
    metro.add_node("Observatorio_L1", pos=(100, 380), linea="L1", nombre="Observatorio")
    metro.add_node("Tacubaya_L1",     pos=(X_L7, Y_L9), linea="L1", nombre="Tacubaya") # HUB
    # Diagonal hacia arriba-derecha
    metro.add_node("Juanacatlan_L1",  pos=(250, 270), linea="L1", nombre="Juanacatlan")
    metro.add_node("Chapultepec_L1",  pos=(320, 220), linea="L1", nombre="Chapultepec")
    metro.add_node("Sevilla_L1",      pos=(390, 170), linea="L1", nombre="Sevilla")
    # Tramo horizontal superior
    metro.add_node("Insurgentes_L1",  pos=(460, 110), linea="L1", nombre="Insurgentes")
    metro.add_node("Cuauhtemoc_L1",   pos=(530, 110), linea="L1", nombre="Cuauhtemoc")
    metro.add_node("Balderas_L1",     pos=(X_L3, 110), linea="L1", nombre="Balderas") # HUB

    
    # --- CONEXIONES (ARISTAS) ---
    
    # L7
    metro.add_edge("Polanco_L7", "Auditorio_L7", weight=2)
    metro.add_edge("Auditorio_L7", "Constituyentes_L7", weight=2)
    metro.add_edge("Constituyentes_L7", "Tacubaya_L7", weight=3)
    metro.add_edge("Tacubaya_L7", "San Pedro de los Pinos_L7", weight=2)
    metro.add_edge("San Pedro de los Pinos_L7", "San Antonio_L7", weight=2)
    metro.add_edge("San Antonio_L7", "Mixcoac_L7", weight=2)
    metro.add_edge("Mixcoac_L7", "Barranca del Muerto_L7", weight=2)

    # L3
    metro.add_edge("Juarez_L3", "Balderas_L3", weight=2)
    metro.add_edge("Balderas_L3", "Ninos Heroes_L3", weight=2)
    metro.add_edge("Ninos Heroes_L3", "Hospital General_L3", weight=2)
    metro.add_edge("Hospital General_L3", "Centro Medico_L3", weight=2)
    metro.add_edge("Centro Medico_L3", "Etiopia_L3", weight=2)
    metro.add_edge("Etiopia_L3", "Eugenia_L3", weight=2)
    metro.add_edge("Eugenia_L3", "Division del Norte_L3", weight=2)
    metro.add_edge("Division del Norte_L3", "Zapata_L3", weight=2)
    metro.add_edge("Zapata_L3", "Coyoacan_L3", weight=2)
    metro.add_edge("Coyoacan_L3", "Viveros_L3", weight=2)
    metro.add_edge("Viveros_L3", "M.A. de Quevedo_L3", weight=2)
    metro.add_edge("M.A. de Quevedo_L3", "Copilco_L3", weight=2)
    metro.add_edge("Copilco_L3", "Universidad_L3", weight=2)

    # L9
    metro.add_edge("Tacubaya_L9", "Patriotismo_L9", weight=3)
    metro.add_edge("Patriotismo_L9", "Chilpancingo_L9", weight=2)
    metro.add_edge("Chilpancingo_L9", "Centro Medico_L9", weight=3)
    metro.add_edge("Centro Medico_L9", "Lazaro Cardenas_L9", weight=2)

    # L12
    metro.add_edge("Mixcoac_L12", "Insurgentes Sur_L12", weight=3)
    metro.add_edge("Insurgentes Sur_L12", "Hospital 20 de Nov_L12", weight=2)
    metro.add_edge("Hospital 20 de Nov_L12", "Zapata_L12", weight=2)
    metro.add_edge("Zapata_L12", "Parque de los Venados_L12", weight=2)
    metro.add_edge("Parque de los Venados_L12", "Eje Central_L12", weight=3)

    # L1
    metro.add_edge("Observatorio_L1", "Tacubaya_L1", weight=3)
    metro.add_edge("Tacubaya_L1", "Juanacatlan_L1", weight=2)
    metro.add_edge("Juanacatlan_L1", "Chapultepec_L1", weight=2)
    metro.add_edge("Chapultepec_L1", "Sevilla_L1", weight=2)
    metro.add_edge("Sevilla_L1", "Insurgentes_L1", weight=2)
    metro.add_edge("Insurgentes_L1", "Cuauhtemoc_L1", weight=2)
    metro.add_edge("Cuauhtemoc_L1", "Balderas_L1", weight=2)

    # --- TRANSBORDOS (Penalización de 5 min) ---
    T_COST = 5
    # Tacubaya (L1, L7, L9)
    metro.add_edge("Tacubaya_L1", "Tacubaya_L7", weight=T_COST)
    metro.add_edge("Tacubaya_L7", "Tacubaya_L9", weight=T_COST)
    metro.add_edge("Tacubaya_L1", "Tacubaya_L9", weight=T_COST)
    
    # Mixcoac (L7, L12)
    metro.add_edge("Mixcoac_L7", "Mixcoac_L12", weight=T_COST)
    
    # Zapata (L3, L12)
    metro.add_edge("Zapata_L3", "Zapata_L12", weight=T_COST)
    
    # Centro Medico (L3, L9)
    metro.add_edge("Centro Medico_L3", "Centro Medico_L9", weight=T_COST)
    
    # Balderas (L1, L3)
    metro.add_edge("Balderas_L1", "Balderas_L3", weight=T_COST)
    
    return metro

# ============================================================================
# 2. ALGORITMO A* (Heurística y Búsqueda)
# ============================================================================

def heuristica(graph, node_a, node_b):
    # Distancia Euclídea usando las coordenadas pos=(x,y)
    x1, y1 = graph.nodes[node_a]['pos']
    x2, y2 = graph.nodes[node_b]['pos']
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Factor de velocidad para convertir píxeles a minutos
    VELOCIDAD = 50.0 
    return dist / VELOCIDAD

def buscar_ruta_a_estrella(graph, start_node, end_node):
    open_set = []
    heapq.heappush(open_set, (0, start_node))
    
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start_node] = 0
    
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start_node] = heuristica(graph, start_node, end_node)
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        
        if current == end_node:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_node)
            path.reverse()
            return path, g_score[end_node]
            
        for neighbor in graph.neighbors(current):
            weight = graph[current][neighbor]['weight']
            tentative_g = g_score[current] + weight
            
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristica(graph, neighbor, end_node)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    return None, 0

# ============================================================================
# 3. INTERFAZ GRÁFICA (Tkinter)
# ============================================================================

class AppMetro:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro CDMX - Ruta Óptima A*")
        self.root.geometry("1000x850") # Ventana más alta para el mapa vertical
        self.root.resizable(True, True)
        
        self.metro_graph = crear_grafo_metro()
        self.nombres_estaciones = sorted(list(set([data['nombre'] for n, data in self.metro_graph.nodes(data=True)])))
        
        # Panel Izquierdo (Controles)
        self.frame_izq = tk.Frame(root, width=250, bg="#f5f5f5", padx=15, pady=15)
        self.frame_izq.pack(side="left", fill="y")
        
        # Panel Derecho (Mapa)
        self.frame_der = tk.Frame(root, bg="white")
        self.frame_der.pack(side="right", fill="both", expand=True)
        
        # Widgets
        tk.Label(self.frame_izq, text="Metro CDMX", font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=(0,20))
        
        tk.Label(self.frame_izq, text="Origen:", bg="#f5f5f5").pack(anchor="w")
        self.combo_origen = ttk.Combobox(self.frame_izq, values=self.nombres_estaciones, state="readonly")
        self.combo_origen.pack(fill="x", pady=5)
        
        tk.Label(self.frame_izq, text="Destino:", bg="#f5f5f5").pack(anchor="w", pady=(15,0))
        self.combo_destino = ttk.Combobox(self.frame_izq, values=self.nombres_estaciones, state="readonly")
        self.combo_destino.pack(fill="x", pady=5)
        
        self.btn_calcular = tk.Button(self.frame_izq, text="BUSCAR RUTA", bg="#FF9800", fg="white", 
                                      font=("Arial", 12, "bold"), command=self.calcular_ruta)
        self.btn_calcular.pack(pady=30, fill="x")
        
        self.lbl_resultado = tk.Label(self.frame_izq, text="", bg="#f5f5f5", font=("Arial", 10), justify="left")
        self.lbl_resultado.pack(pady=10, anchor="w")

        # Canvas
        self.canvas = tk.Canvas(self.frame_der, bg="white")
        self.canvas.pack(fill="both", expand=True)
        
        self.cargar_imagen()

    def cargar_imagen(self):
        try:
            nombre_imagen = "Mapa_metro.jpg"
            imagen_pil = Image.open(nombre_imagen)
            
            # Redimensionamos para que quepa bien en la pantalla
            # El mapa es vertical, así que le damos altura generosa
            self.ancho_mapa = 750
            self.alto_mapa = 800
            imagen_pil = imagen_pil.resize((self.ancho_mapa, self.alto_mapa), Image.Resampling.LANCZOS)
            
            self.mapa_img = ImageTk.PhotoImage(imagen_pil)
            self.canvas.create_image(0, 0, anchor="nw", image=self.mapa_img)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            self.canvas.create_text(300, 300, text=f"No se encuentra: {nombre_imagen}\n{e}", fill="red")

    def get_node_id_by_name(self, name):
        for node, data in self.metro_graph.nodes(data=True):
            if data['nombre'] == name:
                return node
        return None

    def calcular_ruta(self):
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        
        if not origen or not destino:
            messagebox.showwarning("Error", "Selecciona origen y destino")
            return
            
        start_node = self.get_node_id_by_name(origen)
        end_node_candidate = self.get_node_id_by_name(destino)
        
        ruta, tiempo = buscar_ruta_a_estrella(self.metro_graph, start_node, end_node_candidate)
        
        if ruta:
            self.lbl_resultado.config(text=f"Tiempo aprox: {tiempo:.1f} min\nEstaciones: {len(ruta)}")
            self.dibujar_ruta(ruta)
        else:
            messagebox.showinfo("Info", "No se encontró camino.")

    def dibujar_ruta(self, ruta):
        self.canvas.delete("ruta")
        
        for i in range(len(ruta) - 1):
            u = ruta[i]
            v = ruta[i+1]
            
            x1, y1 = self.metro_graph.nodes[u]['pos']
            x2, y2 = self.metro_graph.nodes[v]['pos']
            
            # Línea de trayecto (Azul neón)
            self.canvas.create_line(x1, y1, x2, y2, fill="#00FFFF", width=6, tags="ruta", capstyle=tk.ROUND)
            
            # Estación (Punto Rojo)
            r = 5
            self.canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill="red", outline="white", width=2, tags="ruta")
            self.canvas.create_oval(x2-r, y2-r, x2+r, y2+r, fill="red", outline="white", width=2, tags="ruta")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMetro(root)
    root.mainloop()