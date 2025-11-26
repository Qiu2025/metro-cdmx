import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import networkx as nx
import math
import heapq

# Velocidad media del metro: 36 km/h = 10 m/s
VELOCIDAD_METRO = 10.0  # m/s

# ========================== #
# 1. CONFIGURACIÓN DEL GRAFO #
# ========================== #

def crear_grafo_metro():
    metro = nx.Graph()
    
    # Coordenadas aproximadas basadas en la imagen "Mapa_metro.jpg"
    X_L7 = 190        # Eje vertical izquierdo (Línea Naranja)
    X_L3 = 600        # Eje vertical derecho (Línea Verde Oliva)
    Y_L9 = 290        # Eje horizontal medio (Línea Marrón) - Tacubaya a Centro Medico
    Y_L12 = 550       # Eje horizontal inferior (Línea Dorada) - Mixcoac a Zapata
    
    # ----------------------------------------------------------
    # LÍNEA 7 (Naranja) - Vertical Izquierda
    # ----------------------------------------------------------
    metro.add_node("Polanco_L7",              pos=(X_L7, 22),  linea="L7", nombre="Polanco")
    metro.add_node("Auditorio_L7",            pos=(X_L7, 115), linea="L7", nombre="Auditorio")
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
    metro.add_node("Mixcoac_L12",            pos=(X_L7, Y_L12), linea="L12", nombre="Mixcoac") # HUB
    metro.add_node("Insurgentes Sur_L12",    pos=(320, Y_L12), linea="L12", nombre="Insurgentes Sur")
    metro.add_node("Hospital 20 de Nov_L12", pos=(460, Y_L12), linea="L12", nombre="Hospital 20 de Nov")
    metro.add_node("Zapata_L12",             pos=(X_L3, Y_L12), linea="L12", nombre="Zapata") # HUB
    metro.add_node("Parque de los Venados_L12", pos=(700, Y_L12), linea="L12", nombre="Parque de los Venados")
    metro.add_node("Eje Central_L12",        pos=(740, 620), linea="L12", nombre="Eje Central") # Baja visualmente

    # ----------------------------------------------------------
    # LÍNEA 1 (Rosa) - Diagonal / Horizontal Superior
    # ----------------------------------------------------------
    metro.add_node("Observatorio_L1", pos=(100, 380), linea="L1", nombre="Observatorio")
    metro.add_node("Tacubaya_L1",     pos=(X_L7, Y_L9), linea="L1", nombre="Tacubaya") # HUB
    metro.add_node("Juanacatlan_L1",  pos=(250, 270), linea="L1", nombre="Juanacatlan")
    metro.add_node("Chapultepec_L1",  pos=(320, 220), linea="L1", nombre="Chapultepec")
    metro.add_node("Sevilla_L1",      pos=(390, 170), linea="L1", nombre="Sevilla")
    metro.add_node("Insurgentes_L1",  pos=(460, 110), linea="L1", nombre="Insurgentes")
    metro.add_node("Cuauhtemoc_L1",   pos=(530, 110), linea="L1", nombre="Cuauhtemoc")
    metro.add_node("Balderas_L1",     pos=(X_L3, 110), linea="L1", nombre="Balderas") # HUB

    # ----------------------------------------------------------
    # DISTANCIAS REALES ENTRE ESTACIONES (m)
    # La distancia de cada fila es la distancia entre la estación de la fila y la de abajo.
    # ----------------------------------------------------------
    distancias_reales = {
        # LÍNEA 1
        ("Observatorio_L1", "Tacubaya_L1"): 1262,
        ("Tacubaya_L1", "Juanacatlan_L1"): 1158,
        ("Juanacatlan_L1", "Chapultepec_L1"): 973,
        ("Chapultepec_L1", "Sevilla_L1"): 501,
        ("Sevilla_L1", "Insurgentes_L1"): 645,
        ("Insurgentes_L1", "Cuauhtemoc_L1"): 793,
        ("Cuauhtemoc_L1", "Balderas_L1"): 409,

        # LÍNEA 12
        ("Mixcoac_L12", "Insurgentes Sur_L12"): 651,
        ("Insurgentes Sur_L12", "Hospital 20 de Nov_L12"): 725,
        ("Hospital 20 de Nov_L12", "Zapata_L12"): 450,
        ("Zapata_L12", "Parque de los Venados_L12"): 563,
        ("Parque de los Venados_L12", "Eje Central_L12"): 1280,

        # LÍNEA 9
        ("Tacubaya_L9", "Patriotismo_L9"): 1133,
        ("Patriotismo_L9", "Chilpancingo_L9"): 955,
        ("Chilpancingo_L9", "Centro Medico_L9"): 1152,
        ("Centro Medico_L9", "Lazaro Cardenas_L9"): 1059,

        # LÍNEA 7
        ("Barranca del Muerto_L7", "Mixcoac_L7"): 1476,
        ("Mixcoac_L7", "San Antonio_L7"): 788,
        ("San Antonio_L7", "San Pedro de los Pinos_L7"): 606,
        ("San Pedro de los Pinos_L7", "Tacubaya_L7"): 1084,
        ("Tacubaya_L7", "Constituyentes_L7"): 1005,
        ("Constituyentes_L7", "Auditorio_L7"): 1430,
        ("Auditorio_L7", "Polanco_L7"): 812,

        # LÍNEA 3
        ("Universidad_L3", "Copilco_L3"): 1306,
        ("Copilco_L3", "M.A. de Quevedo_L3"): 1295,
        ("M.A. de Quevedo_L3", "Viveros_L3"): 824,
        ("Viveros_L3", "Coyoacan_L3"): 908,
        ("Coyoacan_L3", "Zapata_L3"): 1153,
        ("Zapata_L3", "Division del Norte_L3"): 794,
        ("Division del Norte_L3", "Eugenia_L3"): 715,
        ("Eugenia_L3", "Etiopia_L3"): 950,
        ("Etiopia_L3", "Centro Medico_L3"): 1119,
        ("Centro Medico_L3", "Hospital General_L3"): 653,
        ("Hospital General_L3", "Ninos Heroes_L3"): 559,
        ("Ninos Heroes_L3", "Balderas_L3"): 665,
        ("Balderas_L3", "Juarez_L3"): 659
    }

    def get_dist(a, b):
        """Devuelve la distancia en metros entre dos estaciones consecutivas."""
        if (a, b) in distancias_reales:
            return distancias_reales[(a, b)]
        if (b, a) in distancias_reales:
            return distancias_reales[(b, a)]
        raise KeyError(f"No se encontró distancia para el tramo {a} - {b}")

    def add_tramo(a, b):
        """Añade un tramo con peso = tiempo en segundos (distancia / velocidad)."""
        dist_m = get_dist(a, b)
        tiempo_seg = dist_m / VELOCIDAD_METRO
        metro.add_edge(a, b, weight=tiempo_seg)

    # --- CONEXIONES (ARISTAS) ---
    # L7
    add_tramo("Polanco_L7", "Auditorio_L7")
    add_tramo("Auditorio_L7", "Constituyentes_L7")
    add_tramo("Constituyentes_L7", "Tacubaya_L7")
    add_tramo("Tacubaya_L7", "San Pedro de los Pinos_L7")
    add_tramo("San Pedro de los Pinos_L7", "San Antonio_L7")
    add_tramo("San Antonio_L7", "Mixcoac_L7")
    add_tramo("Mixcoac_L7", "Barranca del Muerto_L7")

    # L3
    add_tramo("Juarez_L3", "Balderas_L3")
    add_tramo("Balderas_L3", "Ninos Heroes_L3")
    add_tramo("Ninos Heroes_L3", "Hospital General_L3")
    add_tramo("Hospital General_L3", "Centro Medico_L3")
    add_tramo("Centro Medico_L3", "Etiopia_L3")
    add_tramo("Etiopia_L3", "Eugenia_L3")
    add_tramo("Eugenia_L3", "Division del Norte_L3")
    add_tramo("Division del Norte_L3", "Zapata_L3")
    add_tramo("Zapata_L3", "Coyoacan_L3")
    add_tramo("Coyoacan_L3", "Viveros_L3")
    add_tramo("Viveros_L3", "M.A. de Quevedo_L3")
    add_tramo("M.A. de Quevedo_L3", "Copilco_L3")
    add_tramo("Copilco_L3", "Universidad_L3")

    # L9
    add_tramo("Tacubaya_L9", "Patriotismo_L9")
    add_tramo("Patriotismo_L9", "Chilpancingo_L9")
    add_tramo("Chilpancingo_L9", "Centro Medico_L9")
    add_tramo("Centro Medico_L9", "Lazaro Cardenas_L9")

    # L12
    add_tramo("Mixcoac_L12", "Insurgentes Sur_L12")
    add_tramo("Insurgentes Sur_L12", "Hospital 20 de Nov_L12")
    add_tramo("Hospital 20 de Nov_L12", "Zapata_L12")
    add_tramo("Zapata_L12", "Parque de los Venados_L12")
    add_tramo("Parque de los Venados_L12", "Eje Central_L12")

    # L1
    add_tramo("Observatorio_L1", "Tacubaya_L1")
    add_tramo("Tacubaya_L1", "Juanacatlan_L1")
    add_tramo("Juanacatlan_L1", "Chapultepec_L1")
    add_tramo("Chapultepec_L1", "Sevilla_L1")
    add_tramo("Sevilla_L1", "Insurgentes_L1")
    add_tramo("Insurgentes_L1", "Cuauhtemoc_L1")
    add_tramo("Cuauhtemoc_L1", "Balderas_L1")

    # --- TRANSBORDOS (Penalización de 5 min -> 300 s) ---
    T_COST_MIN = 5
    T_COST = T_COST_MIN * 60  # segundos

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

    # -----------------------------
    # Servicios de accesibilidad
    # -----------------------------
    servicios_por_nodo = {
        # Línea 1
        "Observatorio_L1":      {"escalera": False, "ascensor": True},
        "Tacubaya_L1":          {"escalera": True,  "ascensor": False},
        "Juanacatlan_L1":       {"escalera": False, "ascensor": False},
        "Chapultepec_L1":       {"escalera": False, "ascensor": False},
        "Sevilla_L1":           {"escalera": True,  "ascensor": True},
        "Insurgentes_L1":       {"escalera": False, "ascensor": True},
        "Cuauhtemoc_L1":        {"escalera": True,  "ascensor": True},
        "Balderas_L1":          {"escalera": True,  "ascensor": True},

        # Línea 12
        "Mixcoac_L12":          {"escalera": True,  "ascensor": True},
        "Insurgentes Sur_L12":  {"escalera": True,  "ascensor": True},
        "Hospital 20 de Nov_L12":{"escalera": True, "ascensor": True},
        "Zapata_L12":           {"escalera": True,  "ascensor": True},
        "Parque de los Venados_L12":{"escalera": True, "ascensor": True},
        "Eje Central_L12":      {"escalera": True,  "ascensor": True},

        # Línea 9
        "Tacubaya_L9":          {"escalera": True,  "ascensor": False},
        "Patriotismo_L9":       {"escalera": True,  "ascensor": False},
        "Chilpancingo_L9":      {"escalera": True,  "ascensor": False},
        "Centro Medico_L9":     {"escalera": True,  "ascensor": True},
        "Lazaro Cardenas_L9":   {"escalera": False, "ascensor": False},

        # Línea 7
        "Barranca del Muerto_L7":{"escalera": True, "ascensor": False},
        "Mixcoac_L7":           {"escalera": True,  "ascensor": True},
        "San Antonio_L7":       {"escalera": True,  "ascensor": False},
        "San Pedro de los Pinos_L7":{"escalera": True, "ascensor": False},
        "Tacubaya_L7":          {"escalera": True,  "ascensor": False},
        "Constituyentes_L7":    {"escalera": True,  "ascensor": False},
        "Auditorio_L7":         {"escalera": True,  "ascensor": False},
        "Polanco_L7":           {"escalera": True,  "ascensor": False},

        # Línea 3
        "Universidad_L3":       {"escalera": False, "ascensor": True},
        "Copilco_L3":           {"escalera": True,  "ascensor": True},
        "M.A. de Quevedo_L3":   {"escalera": True,  "ascensor": False},
        "Viveros_L3":           {"escalera": True,  "ascensor": False},
        "Coyoacan_L3":          {"escalera": False, "ascensor": False},
        "Zapata_L3":            {"escalera": False, "ascensor": True},
        "Division del Norte_L3":{"escalera": False, "ascensor": False},
        "Eugenia_L3":           {"escalera": False, "ascensor": False},
        "Etiopia_L3":           {"escalera": False, "ascensor": True},
        "Centro Medico_L3":     {"escalera": True,  "ascensor": True},
        "Hospital General_L3":  {"escalera": True,  "ascensor": True},
        "Ninos Heroes_L3":      {"escalera": False, "ascensor": False},
        "Balderas_L3":          {"escalera": True,  "ascensor": True},
        "Juarez_L3":            {"escalera": True,  "ascensor": True},
    }

    # Asignar atributos al grafo
    for node in metro.nodes:
        serv = servicios_por_nodo.get(node, {"escalera": False, "ascensor": False})
        metro.nodes[node]["escalera"] = serv["escalera"]
        metro.nodes[node]["ascensor"] = serv["ascensor"]

    return metro

# ============================================================================
# 2. ALGORITMO A* (Heurística y Búsqueda)
# ============================================================================

def heuristica(graph, node_a, node_b):
    x1, y1 = graph.nodes[node_a]['pos']
    x2, y2 = graph.nodes[node_b]['pos']
    dist_px = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    # Aproximamos 1 píxel ~ 1 metro; devolvemos tiempo estimado en segundos
    return dist_px / VELOCIDAD_METRO

def buscar_ruta_a_estrella(graph, start_node, end_node,
                           require_escalera=False, require_ascensor=False):
    open_set = []
    heapq.heappush(open_set, (0, start_node))
    
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start_node] = 0.0
    
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
            # g_score[end_node] está en segundos
            return path, g_score[end_node]
            
        for neighbor in graph.neighbors(current):
            # Restricción de accesibilidad en TRANSBORDOS
            linea_actual = graph.nodes[current]['linea']
            linea_vecino = graph.nodes[neighbor]['linea']
            if linea_actual != linea_vecino:
                # Es un cambio de línea, aquí sí o sí se usan los servicios
                if require_escalera and (not graph.nodes[current]['escalera'] or not graph.nodes[neighbor]['escalera']):
                    continue
                if require_ascensor and (not graph.nodes[current]['ascensor'] or not graph.nodes[neighbor]['ascensor']):
                    continue

            weight = graph[current][neighbor]['weight']  # segundos
            tentative_g = g_score[current] + weight
            
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristica(graph, neighbor, end_node)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    return None, 0.0

# ============================================================================
# 3. INTERFAZ GRÁFICA (Tkinter)
# ============================================================================

class AppMetro:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro CDMX - Ruta Óptima A*")
        self.root.geometry("1000x850")
        self.root.resizable(True, True)
        
        self.metro_graph = crear_grafo_metro()
        self.nombres_estaciones = sorted(list(set(
            [data['nombre'] for n, data in self.metro_graph.nodes(data=True)]
        )))
        
        self.node_items = {}
        self.last_route_nodes = []

        # Panel Izquierdo (Controles)
        self.frame_izq = tk.Frame(root, width=250, bg="#f5f5f5", padx=15, pady=15)
        self.frame_izq.pack(side="left", fill="y")
        
        # Panel Derecho (Mapa)
        self.frame_der = tk.Frame(root, bg="white")
        self.frame_der.pack(side="right", fill="both", expand=True)
        
        # Widgets básicos
        tk.Label(self.frame_izq, text="Metro CDMX", font=("Arial", 18, "bold"),
                 bg="#f5f5f5").pack(pady=(0,20))
        
        tk.Label(self.frame_izq, text="Origen:", bg="#f5f5f5").pack(anchor="w")
        self.combo_origen = ttk.Combobox(self.frame_izq, values=self.nombres_estaciones, state="readonly")
        self.combo_origen.pack(fill="x", pady=5)
        
        tk.Label(self.frame_izq, text="Destino:", bg="#f5f5f5").pack(anchor="w", pady=(15,0))
        self.combo_destino = ttk.Combobox(self.frame_izq, values=self.nombres_estaciones, state="readonly")
        self.combo_destino.pack(fill="x", pady=5)

        # Filtros de accesibilidad
        tk.Label(self.frame_izq, text="Filtros de accesibilidad:", bg="#f5f5f5",
                 font=("Arial", 11, "bold")).pack(anchor="w", pady=(20,0))
        self.var_escalera = tk.BooleanVar(value=False)
        self.var_ascensor = tk.BooleanVar(value=False)

        tk.Checkbutton(self.frame_izq,
                       text="Requiere escaleras electromecánicas",
                       variable=self.var_escalera,
                       bg="#f5f5f5").pack(anchor="w")
        tk.Checkbutton(self.frame_izq,
                       text="Requiere ascensor",
                       variable=self.var_ascensor,
                       bg="#f5f5f5").pack(anchor="w")
        
        self.btn_calcular = tk.Button(self.frame_izq, text="BUSCAR RUTA",
                                      bg="#FF9800", fg="white", 
                                      font=("Arial", 12, "bold"),
                                      command=self.calcular_ruta)
        self.btn_calcular.pack(pady=20, fill="x")
        
        self.lbl_resultado = tk.Label(self.frame_izq, text="", bg="#f5f5f5",
                                      font=("Arial", 10), justify="left")
        self.lbl_resultado.pack(pady=10, anchor="w")

        # Canvas
        self.canvas = tk.Canvas(self.frame_der, bg="white")
        self.canvas.pack(fill="both", expand=True)
        
        self.cargar_imagen()

        # === Dibujar todo el grafo ===
        # Aristas
        for u, v in self.metro_graph.edges():
            x1, y1 = self.metro_graph.nodes[u]['pos']
            x2, y2 = self.metro_graph.nodes[v]['pos']
            self.canvas.create_line(x1, y1, x2, y2, fill="#999999", width=2, tags="grafo")

        # Nodos clicables
        for node, data in self.metro_graph.nodes(data=True):
            x, y = data['pos']
            r = 10   # tamaño más grande
            item = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill="black",
                outline="white",
                width=2,
                tags=("grafo", "nodo")
            )

            self.node_items[node] = item

            self.canvas.tag_bind(
                item,
                "<Button-1>",
                lambda e, n=node: self.on_node_click(n)
            )

    def cargar_imagen(self):
        try:
            nombre_imagen = "Mapa_metro.jpg"
            imagen_pil = Image.open(nombre_imagen)
            self.ancho_mapa = 750
            self.alto_mapa = 800
            imagen_pil = imagen_pil.resize((self.ancho_mapa, self.alto_mapa),
                                           Image.Resampling.LANCZOS)
            self.mapa_img = ImageTk.PhotoImage(imagen_pil)
            self.canvas.create_image(0, 0, anchor="nw", image=self.mapa_img)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        except Exception as e:
            self.canvas.create_text(300, 300,
                                    text=f"No se encuentra: {nombre_imagen}\n{e}",
                                    fill="red")

    def get_node_id_by_name(self, name):
        # Devuelve UN nodo cualquiera con ese nombre (si hay varios, por ejemplo Zapata, coge uno)
        for node, data in self.metro_graph.nodes(data=True):
            if data['nombre'] == name:
                return node
        return None

    def tiene_servicios(self, node_id, require_escalera, require_ascensor):
        data = self.metro_graph.nodes[node_id]
        if require_escalera and not data['escalera']:
            return False
        if require_ascensor and not data['ascensor']:
            return False
        return True

    def on_node_click(self, node_id):
        nombre_estacion = self.metro_graph.nodes[node_id]['nombre']
        esc = "Sí" if self.metro_graph.nodes[node_id]['escalera'] else "No"
        asc = "Sí" if self.metro_graph.nodes[node_id]['ascensor'] else "No"

        origen = self.combo_origen.get()
        destino = self.combo_destino.get()

        if not origen:
            self.combo_origen.set(nombre_estacion)
        elif not destino:
            self.combo_destino.set(nombre_estacion)
        else:
            self.combo_origen.set(nombre_estacion)
            self.combo_destino.set("")

        self.lbl_resultado.config(
            text=f"Estación seleccionada: {nombre_estacion}\n"
                 f"Escaleras: {esc}  Ascensor: {asc}"
        )

    def calcular_ruta(self):
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        
        if not origen or not destino:
            messagebox.showwarning("Error", "Selecciona origen y destino")
            return
        
        start_node = self.get_node_id_by_name(origen)
        end_node = self.get_node_id_by_name(destino)

        if start_node is None or end_node is None:
            messagebox.showwarning("Error", "No se encontraron las estaciones en el grafo.")
            return

        require_escalera = self.var_escalera.get()
        require_ascensor = self.var_ascensor.get()

        # El origen y el destino deben cumplir los filtros seleccionados
        if not self.tiene_servicios(start_node, require_escalera, require_ascensor):
            messagebox.showwarning(
                "Accesibilidad",
                "La estación de origen no dispone de los servicios seleccionados."
            )
            return

        if not self.tiene_servicios(end_node, require_escalera, require_ascensor):
            messagebox.showwarning(
                "Accesibilidad",
                "La estación de destino no dispone de los servicios seleccionados."
            )
            return
        
        ruta, tiempo_seg = buscar_ruta_a_estrella(
            self.metro_graph, start_node, end_node,
            require_escalera=require_escalera,
            require_ascensor=require_ascensor
        )
        
        if ruta:
            # Convertir de segundos a minutos y redondear hacia arriba
            tiempo_min = math.ceil(tiempo_seg / 60.0)
            self.lbl_resultado.config(
                text=f"Tiempo aprox: {tiempo_min} min\nEstaciones: {len(ruta)}"
            )
            self.dibujar_ruta(ruta)
        else:
            messagebox.showinfo(
                "Info",
                "No se encontró un camino que cumpla los filtros de accesibilidad."
            )

    def dibujar_ruta(self, ruta):
        self.canvas.delete("ruta")

        for n in self.last_route_nodes:
            item = self.node_items.get(n)
            if item:
                self.canvas.itemconfig(item, fill="black", outline="white", width=1)

        self.last_route_nodes = ruta[:]

        for i in range(len(ruta) - 1):
            u = ruta[i]
            v = ruta[i+1]
            x1, y1 = self.metro_graph.nodes[u]['pos']
            x2, y2 = self.metro_graph.nodes[v]['pos']
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#00FFFF", width=6, tags="ruta", capstyle=tk.ROUND
            )

        for n in ruta:
            item = self.node_items.get(n)
            if item:
                self.canvas.itemconfig(item, fill="red", outline="white", width=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMetro(root)
    root.mainloop()
