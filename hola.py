import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageOps
import networkx as nx
import math
import heapq
import os
import json 


def crear_grafo_metro():
    metro = nx.Graph()
    
    # 1. Intentar cargar las coordenadas del archivo JSON
    coords = {}
    if os.path.exists("coordenadas_metro.json"):
        with open("coordenadas_metro.json", "r") as f:
            coords = json.load(f)
    else:
        print("ALERTA: No encontré coordenadas_metro.json. Ejecuta el mapeador primero.")
        # Coordenadas dummy para que no falle si no hay archivo
        coords = {nombre: (0,0) for nombre in [
            "Polanco", "Auditorio", "Constituyentes", "Tacubaya", "Mixcoac", 
            "Barranca del Muerto", "Balderas", "Centro Medico", "Zapata"
            # ... etc
        ]}

    # Helper para obtener posición de forma segura
    def get_pos(nombre):
        return coords.get(nombre, (0, 0)) # Retorna (0,0) si no existe el nombre

    # --- AGREGAR NODOS USANDO EL JSON ---
    
    # L7
    metro.add_node("Polanco",       pos=get_pos("Polanco"), linea="L7", nombre="Polanco")
    metro.add_node("Auditorio",     pos=get_pos("Auditorio"), linea="L7", nombre="Auditorio")
    metro.add_node("Constituyentes",pos=get_pos("Constituyentes"), linea="L7", nombre="Constituyentes")
    metro.add_node("Tacubaya",      pos=get_pos("Tacubaya"), linea="HUB", nombre="Tacubaya")
    metro.add_node("San Pedro de los Pinos", pos=get_pos("San Pedro de los Pinos"), linea="L7", nombre="San Pedro de los Pinos")
    metro.add_node("San Antonio",   pos=get_pos("San Antonio"), linea="L7", nombre="San Antonio")
    metro.add_node("Mixcoac",       pos=get_pos("Mixcoac"), linea="HUB", nombre="Mixcoac")
    metro.add_node("Barranca del Muerto", pos=get_pos("Barranca del Muerto"), linea="L7", nombre="Barranca del Muerto")

    # L3
    metro.add_node("Juarez",        pos=get_pos("Juarez"), linea="L3", nombre="Juarez")
    metro.add_node("Balderas",      pos=get_pos("Balderas"), linea="HUB", nombre="Balderas")
    metro.add_node("Ninos Heroes",  pos=get_pos("Ninos Heroes"), linea="L3", nombre="Ninos Heroes")
    metro.add_node("Hospital General", pos=get_pos("Hospital General"), linea="L3", nombre="Hospital General")
    metro.add_node("Centro Medico", pos=get_pos("Centro Medico"), linea="HUB", nombre="Centro Medico")
    metro.add_node("Etiopia",       pos=get_pos("Etiopia"), linea="L3", nombre="Etiopia")
    metro.add_node("Eugenia",       pos=get_pos("Eugenia"), linea="L3", nombre="Eugenia")
    metro.add_node("Division del Norte", pos=get_pos("Division del Norte"), linea="L3", nombre="Division del Norte")
    metro.add_node("Zapata",        pos=get_pos("Zapata"), linea="HUB", nombre="Zapata")
    metro.add_node("Coyoacan",      pos=get_pos("Coyoacan"), linea="L3", nombre="Coyoacan")
    metro.add_node("Viveros",       pos=get_pos("Viveros"), linea="L3", nombre="Viveros")
    metro.add_node("M.A. de Quevedo", pos=get_pos("M.A. de Quevedo"), linea="L3", nombre="M.A. de Quevedo")
    metro.add_node("Copilco",       pos=get_pos("Copilco"), linea="L3", nombre="Copilco")
    metro.add_node("Universidad",   pos=get_pos("Universidad"), linea="L3", nombre="Universidad")

    # L1
    metro.add_node("Observatorio",  pos=get_pos("Observatorio"), linea="L1", nombre="Observatorio")
    metro.add_node("Juanacatlan",   pos=get_pos("Juanacatlan"), linea="L1", nombre="Juanacatlan")
    metro.add_node("Chapultepec",   pos=get_pos("Chapultepec"), linea="L1", nombre="Chapultepec")
    metro.add_node("Sevilla",       pos=get_pos("Sevilla"), linea="L1", nombre="Sevilla")
    metro.add_node("Insurgentes",   pos=get_pos("Insurgentes"), linea="L1", nombre="Insurgentes")
    metro.add_node("Cuauhtemoc",    pos=get_pos("Cuauhtemoc"), linea="L1", nombre="Cuauhtemoc")

    # L9
    metro.add_node("Patriotismo",   pos=get_pos("Patriotismo"), linea="L9", nombre="Patriotismo")
    metro.add_node("Chilpancingo",  pos=get_pos("Chilpancingo"), linea="L9", nombre="Chilpancingo")
    metro.add_node("Lazaro Cardenas", pos=get_pos("Lazaro Cardenas"), linea="L9", nombre="Lazaro Cardenas")

    # L12
    metro.add_node("Insurgentes Sur", pos=get_pos("Insurgentes Sur"), linea="L12", nombre="Insurgentes Sur")
    metro.add_node("Hospital 20 de Nov", pos=get_pos("Hospital 20 de Nov"), linea="L12", nombre="Hospital 20 de Nov")
    metro.add_node("Parque de los Venados", pos=get_pos("Parque de los Venados"), linea="L12", nombre="Parque de los Venados")
    metro.add_node("Eje Central",   pos=get_pos("Eje Central"), linea="L12", nombre="Eje Central")

    # --- DEFINIR LAS CONEXIONES (ARISTAS) ---
    # (El código de las conexiones add_edge se mantiene IGUAL que antes, no cambia)
    # L7
    metro.add_edge("Polanco", "Auditorio", weight=2)
    metro.add_edge("Auditorio", "Constituyentes", weight=2)
    metro.add_edge("Constituyentes", "Tacubaya", weight=3)
    metro.add_edge("Tacubaya", "San Pedro de los Pinos", weight=2)
    metro.add_edge("San Pedro de los Pinos", "San Antonio", weight=2)
    metro.add_edge("San Antonio", "Mixcoac", weight=2)
    metro.add_edge("Mixcoac", "Barranca del Muerto", weight=2)

    # L3
    metro.add_edge("Juarez", "Balderas", weight=2)
    metro.add_edge("Balderas", "Ninos Heroes", weight=2)
    metro.add_edge("Ninos Heroes", "Hospital General", weight=2)
    metro.add_edge("Hospital General", "Centro Medico", weight=2)
    metro.add_edge("Centro Medico", "Etiopia", weight=2)
    metro.add_edge("Etiopia", "Eugenia", weight=2)
    metro.add_edge("Eugenia", "Division del Norte", weight=2)
    metro.add_edge("Division del Norte", "Zapata", weight=2)
    metro.add_edge("Zapata", "Coyoacan", weight=2)
    metro.add_edge("Coyoacan", "Viveros", weight=2)
    metro.add_edge("Viveros", "M.A. de Quevedo", weight=2)
    metro.add_edge("M.A. de Quevedo", "Copilco", weight=2)
    metro.add_edge("Copilco", "Universidad", weight=2)

    # L1
    metro.add_edge("Observatorio", "Tacubaya", weight=3)
    metro.add_edge("Tacubaya", "Juanacatlan", weight=2)
    metro.add_edge("Juanacatlan", "Chapultepec", weight=2)
    metro.add_edge("Chapultepec", "Sevilla", weight=2)
    metro.add_edge("Sevilla", "Insurgentes", weight=2)
    metro.add_edge("Insurgentes", "Cuauhtemoc", weight=2)
    metro.add_edge("Cuauhtemoc", "Balderas", weight=2)

    # L9
    metro.add_edge("Tacubaya", "Patriotismo", weight=3)
    metro.add_edge("Patriotismo", "Chilpancingo", weight=2)
    metro.add_edge("Chilpancingo", "Centro Medico", weight=3)
    metro.add_edge("Centro Medico", "Lazaro Cardenas", weight=2)

    # L12
    metro.add_edge("Mixcoac", "Insurgentes Sur", weight=3)
    metro.add_edge("Insurgentes Sur", "Hospital 20 de Nov", weight=2)
    metro.add_edge("Hospital 20 de Nov", "Zapata", weight=2)
    metro.add_edge("Zapata", "Parque de los Venados", weight=2)
    metro.add_edge("Parque de los Venados", "Eje Central", weight=3)

    return metro

# ============================================================================
# 3. ALGORITMO A*
# ============================================================================

def heuristica(graph, node_a, node_b):
    x1, y1 = graph.nodes[node_a]['pos']
    x2, y2 = graph.nodes[node_b]['pos']
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist / 50.0 # Factor arbitrario px a minutos

def buscar_ruta_a_estrella(graph, start_node, end_node):
    if start_node not in graph or end_node not in graph:
        return None, 0
        
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
# 4. INTERFAZ GRÁFICA (Clase Principal)
# ============================================================================

class AppMetro:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro CDMX - Ruta Óptima A*")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)

        # Cargar datos
        self.metro_graph = crear_grafo_metro()
        self.nombres_estaciones = sorted(list(set([data['nombre'] for n, data in self.metro_graph.nodes(data=True)])))
        
        # Variables de visualización
        self.ruta_actual = None
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        # --- LAYOUT ---
        # Panel Izquierdo
        self.frame_izq = tk.Frame(root, width=250, bg="#f5f5f5", padx=20, pady=20)
        self.frame_izq.pack(side="left", fill="y")
        
        # Panel Derecho (Mapa)
        self.frame_der = tk.Frame(root, bg="#2b2b2b")
        self.frame_der.pack(side="right", fill="both", expand=True)
        
        # --- CONTROLES IZQUIERDA ---
        tk.Label(self.frame_izq, text="Metro CDMX", font=("Helvetica", 20, "bold"), bg="#f5f5f5", fg="#333").pack(pady=(0,30))
        
        tk.Label(self.frame_izq, text="Origen:", bg="#f5f5f5", font=("Arial", 11)).pack(anchor="w")
        self.combo_origen = ttk.Combobox(self.frame_izq, values=self.nombres_estaciones, state="readonly")
        self.combo_origen.pack(fill="x", pady=(5, 20))
        
        tk.Label(self.frame_izq, text="Destino:", bg="#f5f5f5", font=("Arial", 11)).pack(anchor="w")
        self.combo_destino = ttk.Combobox(self.frame_izq, values=self.nombres_estaciones, state="readonly")
        self.combo_destino.pack(fill="x", pady=(5, 20))
        
        self.btn_calcular = tk.Button(self.frame_izq, text="BUSCAR RUTA", bg="#007aff", fg="white", 
                                      font=("Arial", 12, "bold"), relief="flat", padx=10, pady=5,
                                      command=self.calcular_ruta)
        self.btn_calcular.pack(pady=20, fill="x")
        
        self.lbl_resultado = tk.Label(self.frame_izq, text="Selecciona estaciones...", bg="#f5f5f5", 
                                      font=("Arial", 10), justify="left", fg="#555")
        self.lbl_resultado.pack(pady=10, anchor="w")

        # --- CANVAS ---
        self.canvas = tk.Canvas(self.frame_der, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Cargar imagen inicial (Color)
        self.cargar_imagen("Mapa_metro.png")

        # --- EVENTOS ---
        # Detectar redimensionamiento de ventana
        self.canvas.bind("<Configure>", self.on_resize)
        # Detectar CLIC para calibrar coordenadas
        self.canvas.bind("<Button-1>", self.obtener_coords_click)

    def cargar_imagen(self, path):
        if not os.path.exists(path):
            # Fallback si no existe la recortada, usa la original
            path_orig = path.replace("_sin_margen", "")
            if os.path.exists(path_orig):
                path = path_orig
            else:
                self.canvas.create_text(200, 200, text=f"ERROR: No imagen {path}", fill="red")
                return

        self.img_pil_original = Image.open(path)
        self.orig_w, self.orig_h = self.img_pil_original.size
        self.redibujar_todo()

    def on_resize(self, event):
        self.redibujar_todo()

    def redibujar_todo(self):
        """ Redibuja la imagen de fondo y el grafo sobrepuesto ajustado """
        self.canvas.delete("all")
        
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        
        if cw < 10 or ch < 10: return

        # 1. Calcular Escala (Aspect Ratio 'contain')
        ratio_w = cw / self.orig_w
        ratio_h = ch / self.orig_h
        self.scale = min(ratio_w, ratio_h)
        
        new_w = int(self.orig_w * self.scale)
        new_h = int(self.orig_h * self.scale)
        
        # 2. Calcular Offset (Centrado)
        self.offset_x = (cw - new_w) // 2
        self.offset_y = (ch - new_h) // 2
        
        # 3. Dibujar Imagen
        img_resized = self.img_pil_original.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img_resized)
        
        self.canvas.create_image(cw//2, ch//2, anchor="center", image=self.tk_image)
        
        # 4. Dibujar Ruta (si existe)
        if self.ruta_actual:
            self.dibujar_ruta_sobre_canvas(self.ruta_actual)

    def transformar_coord(self, original_x, original_y):
        """ Transforma coordenadas de la imagen original -> Coordenadas de pantalla actual """
        screen_x = (original_x * self.scale) + self.offset_x
        screen_y = (original_y * self.scale) + self.offset_y
        return screen_x, screen_y

    def obtener_coords_click(self, event):
        """ 
        HERRAMIENTA DE CALIBRACIÓN:
        Al hacer click, imprime en la consola la coordenada (X, Y) 
        perteneciente a la imagen original.
        """
        if self.scale == 0: return
        
        real_x = int((event.x - self.offset_x) / self.scale)
        real_y = int((event.y - self.offset_y) / self.scale)
        
        print(f"--- CALIBRACIÓN ---")
        print(f"Click en pantalla: ({event.x}, {event.y})")
        print(f"COORDENADA PARA EL JSON: ({real_x}, {real_y})")
        print("-------------------")

    def calcular_ruta(self):
        origen_nombre = self.combo_origen.get()
        destino_nombre = self.combo_destino.get()
        
        if not origen_nombre or not destino_nombre:
            messagebox.showwarning("Atención", "Selecciona origen y destino")
            return
        
        # Buscar ID de nodos
        start = next((n for n, d in self.metro_graph.nodes(data=True) if d['nombre'] == origen_nombre), None)
        end = next((n for n, d in self.metro_graph.nodes(data=True) if d['nombre'] == destino_nombre), None)
        
        if not start or not end:
            return

        ruta, tiempo = buscar_ruta_a_estrella(self.metro_graph, start, end)
        
        if ruta:
            self.ruta_actual = ruta
            self.lbl_resultado.config(text=f"Tiempo estimado: {tiempo:.1f} min\nEstaciones: {len(ruta)}")
            
            # Cambiar a Mapa B/N para resaltar la ruta (si existe el archivo)
            # Verifica si la imagen actual ya es la versión BN
            if "BN" not in self.img_pil_original.filename:
                path_bn = "Mapa_metro_BN.png"
                if os.path.exists(path_bn):
                    self.cargar_imagen(path_bn)
                else:
                    self.redibujar_todo()
            else:
                self.redibujar_todo()
        else:
            messagebox.showinfo("Ups", "No se encontró un camino posible.")

    def dibujar_ruta_sobre_canvas(self, ruta):
        """ Dibuja la ruta con líneas gruesas y destaca Inicio/Fin """
        
        # --- CONFIGURACIÓN DE ESTILO ---
        color_linea = "#00FFFF"      # Cyan Neón
        color_nodo_normal = "#FF0000" # Rojo (intermedios)
        color_inicio = "#00FF00"      # Verde (Origen)
        color_fin = "#FFD700"         # Dorado (Destino)
        
        # Factores de escala
        factor_grosor = 12       # Grosor de la línea
        factor_radio_normal = 6  # Tamaño nodos intermedios
        factor_radio_destacado = 25 # Tamaño nodos Inicio/Fin (Más grandes)
        
        # Calcular tamaños dinámicos según el zoom
        ancho_linea = max(4, int(factor_grosor * self.scale)) 
        r_normal = max(4, int(factor_radio_normal * self.scale))
        r_destacado = max(6, int(factor_radio_destacado * self.scale))
        
        # 1. DIBUJAR LÍNEAS (ARISTAS)
        # Recorremos toda la ruta para pintar las conexiones
        for i in range(len(ruta) - 1):
            u = ruta[i]
            v = ruta[i+1]
            
            # Coordenadas originales
            raw_x1, raw_y1 = self.metro_graph.nodes[u]['pos']
            raw_x2, raw_y2 = self.metro_graph.nodes[v]['pos']
            
            # Transformar a pantalla
            x1, y1 = self.transformar_coord(raw_x1, raw_y1)
            x2, y2 = self.transformar_coord(raw_x2, raw_y2)
            
            # Dibujar línea
            self.canvas.create_line(x1, y1, x2, y2, fill=color_linea, width=ancho_linea, 
                                    capstyle=tk.ROUND, joinstyle=tk.ROUND, tags="ruta")

        # 2. DIBUJAR TODOS LOS NODOS (Tamaño normal)
        for nodo in ruta:
            raw_x, raw_y = self.metro_graph.nodes[nodo]['pos']
            x, y = self.transformar_coord(raw_x, raw_y)
            
            self.canvas.create_oval(x-r_normal, y-r_normal, x+r_normal, y+r_normal, 
                                    fill=color_nodo_normal, outline="white", width=2, tags="ruta")

        # 3. SOBRESCRIBIR INICIO Y FIN (Tamaño Grande)
        # --- Nodo Inicial (Origen) ---
        nodo_inicio = ruta[0]
        raw_xi, raw_yi = self.metro_graph.nodes[nodo_inicio]['pos']
        xi, yi = self.transformar_coord(raw_xi, raw_yi)
        
        self.canvas.create_oval(xi-r_destacado, yi-r_destacado, xi+r_destacado, yi+r_destacado, 
                                fill=color_inicio, outline="black", width=3, tags="ruta")
        
        # --- Nodo Final (Destino) ---
        nodo_fin = ruta[-1]
        raw_xf, raw_yf = self.metro_graph.nodes[nodo_fin]['pos']
        xf, yf = self.transformar_coord(raw_xf, raw_yf)
        
        self.canvas.create_oval(xf-r_destacado, yf-r_destacado, xf+r_destacado, yf+r_destacado, 
                                fill=color_fin, outline="black", width=3, tags="ruta")

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AppMetro(root)
    root.mainloop()