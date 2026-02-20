import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import networkx as nx
import math
import heapq
import json

# =============================================================
# CONSTANTES
# =============================================================
PENALIZACION = 300  # Penalización por transbordo (5 minutos)
TIEMPO_PARADA = 30  # Tiempo de parada en cada estación
VELOCIDAD_METRO = 10.0  # m/s

# Latitud y longitud
LAT_LON = {
    "Observatorio_L1": (19.398333, -99.200278),
    "Tacubaya_L1": (19.403333, -99.187222),
    "Juanacatlan_L1": (19.412778, -99.182222),
    "Chapultepec_L1": (19.420833, -99.176389),
    "Sevilla_L1": (19.421944, -99.170556),
    "Insurgentes_L1": (19.423333, -99.163056),
    "Cuauhtemoc_L1": (19.425833, -99.154722),
    "Balderas_L1": (19.427500, -99.149167),

    "Mixcoac_L12": (19.375833, -99.187500),
    "Insurgentes Sur_L12": (19.373611, -99.178889),
    "Hospital 20 de Nov_L12": (19.371944, -99.171111),
    "Zapata_L12": (19.370833, -99.165000),
    "Parque de los Venados_L12": (19.370833, -99.158611),
    "Eje Central_L12": (19.361389, -99.151389),

    "Tacubaya_L9": (19.403333, -99.187222),
    "Patriotismo_L9": (19.406111, -99.178889),
    "Chilpancingo_L9": (19.405833, -99.168611),
    "Centro Medico_L9": (19.406667, -99.155833),
    "Lazaro Cardenas_L9": (19.406944, -99.145000),

    "Barranca del Muerto_L7": (19.360556, -99.190278),
    "Mixcoac_L7": (19.375833, -99.187500),
    "San Antonio_L7": (19.384722, -99.186389),
    "San Pedro de los Pinos_L7": (19.391389, -99.186111),
    "Tacubaya_L7": (19.403333, -99.187222),
    "Constituyentes_L7": (19.411944, -99.191389),
    "Auditorio_L7": (19.425556, -99.191944),
    "Polanco_L7": (19.433611, -99.191111),

    "Universidad_L3": (19.324444, -99.173889),
    "Copilco_L3": (19.335833, -99.176667),
    "M.A. de Quevedo_L3": (19.346389, -99.181111),
    "Viveros_L3": (19.353611, -99.176111),
    "Coyoacan_L3": (19.361389, -99.170833),
    "Zapata_L3": (19.370833, -99.165000),
    "Division del Norte_L3": (19.380000, -99.158889),
    "Eugenia_L3": (19.385556, -99.157500),
    "Etiopia_L3": (19.395556, -99.156389),
    "Centro Medico_L3": (19.406667, -99.155833),
    "Hospital General_L3": (19.413611, -99.153889),
    "Ninos Heroes_L3": (19.419444, -99.150556),
    "Balderas_L3": (19.427500, -99.149167),
    "Juarez_L3": (19.433056, -99.147778)
}

DISTANCIAS_REALES = {
    ("Polanco_L7","Auditorio_L7"):812,
    ("Auditorio_L7","Constituyentes_L7"):1430,
    ("Constituyentes_L7","Tacubaya_L7"):1005,
    ("Tacubaya_L7","San Pedro de los Pinos_L7"):1084,
    ("San Pedro de los Pinos_L7","San Antonio_L7"):606,
    ("San Antonio_L7","Mixcoac_L7"):788,
    ("Mixcoac_L7","Barranca del Muerto_L7"):1476,

    ("Juarez_L3","Balderas_L3"):659,
    ("Balderas_L3","Ninos Heroes_L3"):665,
    ("Ninos Heroes_L3","Hospital General_L3"):559,
    ("Hospital General_L3","Centro Medico_L3"):653,
    ("Centro Medico_L3","Etiopia_L3"):1119,
    ("Etiopia_L3","Eugenia_L3"):950,
    ("Eugenia_L3","Division del Norte_L3"):715,
    ("Division del Norte_L3","Zapata_L3"):794,
    ("Zapata_L3","Coyoacan_L3"):1153,
    ("Coyoacan_L3","Viveros_L3"):908,
    ("Viveros_L3","M.A. de Quevedo_L3"):824,
    ("M.A. de Quevedo_L3","Copilco_L3"):1295,
    ("Copilco_L3","Universidad_L3"):1306,

    ("Tacubaya_L9","Patriotismo_L9"):1133,
    ("Patriotismo_L9","Chilpancingo_L9"):955,
    ("Chilpancingo_L9","Centro Medico_L9"):1152,
    ("Centro Medico_L9","Lazaro Cardenas_L9"):1059,

    ("Mixcoac_L12","Insurgentes Sur_L12"):651,
    ("Insurgentes Sur_L12","Hospital 20 de Nov_L12"):725,
    ("Hospital 20 de Nov_L12","Zapata_L12"):450,
    ("Zapata_L12","Parque de los Venados_L12"):563,
    ("Parque de los Venados_L12","Eje Central_L12"):1280,

    ("Observatorio_L1","Tacubaya_L1"):1262,
    ("Tacubaya_L1","Juanacatlan_L1"):1158,
    ("Juanacatlan_L1","Chapultepec_L1"):973,
    ("Chapultepec_L1","Sevilla_L1"):501,
    ("Sevilla_L1","Insurgentes_L1"):645,
    ("Insurgentes_L1","Cuauhtemoc_L1"):793,
    ("Cuauhtemoc_L1","Balderas_L1"):409,
}

# =============================================================
# A* y búsquedas
# =============================================================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0  # radio medio de la Tierra en metros
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def heuristica(graph, node_a, node_b):
    lat1, lon1 = LAT_LON[node_a]
    lat2, lon2 = LAT_LON[node_b]
    dist_metros = haversine(lat1, lon1, lat2, lon2)
    return dist_metros / VELOCIDAD_METRO

def astar_path(grafo, inicio, fin):
    heur_cache = {n: heuristica(grafo, n, fin) for n in grafo.nodes}

    open_set = []
    g = {n: float("inf") for n in grafo.nodes}
    f = {n: float("inf") for n in grafo.nodes}
    g[inicio] = 0.0
    f[inicio] = heur_cache[inicio]
    heapq.heappush(open_set, (f[inicio], inicio))

    came = {}
    closed = set()
    adj = grafo.adj

    while open_set:
        current_f, current = heapq.heappop(open_set)
        if current_f > f[current]:
            continue

        if current == fin:
            ruta = []
            while current in came:
                ruta.append(current)
                current = came[current]
            ruta.append(inicio)
            ruta.reverse()
            return ruta, g[fin]

        if current in closed:
            continue
        closed.add(current)

        for nb, attr in adj[current].items():
            peso = attr.get("weight", 0.0)
            ng = g[current] + peso
            if ng < g[nb]:
                g[nb] = ng
                came[nb] = current
                f[nb] = ng + heur_cache[nb]
                heapq.heappush(open_set, (f[nb], nb))

    return None, 0

# =============================================================
# GRAFO
# =============================================================
def crear_grafo():
    G = nx.Graph()

    with open("coordenadas_metro.json", "r") as f:
        coords = json.load(f)

    def P(n):
        if n in coords:
            return coords[n]
        return (0, 0)

    # ---------------------------------------------------------
    # 1. NODOS
    # ---------------------------------------------------------

    # Línea 7
    G.add_node("Polanco_L7", pos=P("Polanco"), linea="L7", nombre="Polanco")
    G.add_node("Auditorio_L7", pos=P("Auditorio"), linea="L7", nombre="Auditorio")
    G.add_node("Constituyentes_L7", pos=P("Constituyentes"), linea="L7", nombre="Constituyentes")
    G.add_node("Tacubaya_L7", pos=P("Tacubaya"), linea="L7", nombre="Tacubaya")
    G.add_node("San Pedro de los Pinos_L7", pos=P("San Pedro de los Pinos"), linea="L7", nombre="San Pedro de los Pinos")
    G.add_node("San Antonio_L7", pos=P("San Antonio"), linea="L7", nombre="San Antonio")
    G.add_node("Mixcoac_L7", pos=P("Mixcoac"), linea="L7", nombre="Mixcoac")
    G.add_node("Barranca del Muerto_L7", pos=P("Barranca del Muerto"), linea="L7", nombre="Barranca del Muerto")

    # Línea 3
    G.add_node("Juarez_L3", pos=P("Juarez"), linea="L3", nombre="Juarez")
    G.add_node("Balderas_L3", pos=P("Balderas"), linea="L3", nombre="Balderas")
    G.add_node("Ninos Heroes_L3", pos=P("Ninos Heroes"), linea="L3", nombre="Ninos Heroes")
    G.add_node("Hospital General_L3", pos=P("Hospital General"), linea="L3", nombre="Hospital General")
    G.add_node("Centro Medico_L3", pos=P("Centro Medico"), linea="L3", nombre="Centro Medico")
    G.add_node("Etiopia_L3", pos=P("Etiopia"), linea="L3", nombre="Etiopia")
    G.add_node("Eugenia_L3", pos=P("Eugenia"), linea="L3", nombre="Eugenia")
    G.add_node("Division del Norte_L3", pos=P("Division del Norte"), linea="L3", nombre="Division del Norte")
    G.add_node("Zapata_L3", pos=P("Zapata"), linea="L3", nombre="Zapata")
    G.add_node("Coyoacan_L3", pos=P("Coyoacan"), linea="L3", nombre="Coyoacan")
    G.add_node("Viveros_L3", pos=P("Viveros"), linea="L3", nombre="Viveros")
    G.add_node("M.A. de Quevedo_L3", pos=P("M.A. de Quevedo"), linea="L3", nombre="M.A. de Quevedo")
    G.add_node("Copilco_L3", pos=P("Copilco"), linea="L3", nombre="Copilco")
    G.add_node("Universidad_L3", pos=P("Universidad"), linea="L3", nombre="Universidad")

    # Línea 9
    G.add_node("Tacubaya_L9", pos=P("Tacubaya"), linea="L9", nombre="Tacubaya")
    G.add_node("Patriotismo_L9", pos=P("Patriotismo"), linea="L9", nombre="Patriotismo")
    G.add_node("Chilpancingo_L9", pos=P("Chilpancingo"), linea="L9", nombre="Chilpancingo")
    G.add_node("Centro Medico_L9", pos=P("Centro Medico"), linea="L9", nombre="Centro Medico")
    G.add_node("Lazaro Cardenas_L9", pos=P("Lazaro Cardenas"), linea="L9", nombre="Lazaro Cardenas")

    # Línea 12
    G.add_node("Mixcoac_L12", pos=P("Mixcoac"), linea="L12", nombre="Mixcoac")
    G.add_node("Insurgentes Sur_L12", pos=P("Insurgentes Sur"), linea="L12", nombre="Insurgentes Sur")
    G.add_node("Hospital 20 de Nov_L12", pos=P("Hospital 20 de Nov"), linea="L12", nombre="Hospital 20 de Nov")
    G.add_node("Zapata_L12", pos=P("Zapata"), linea="L12", nombre="Zapata")
    G.add_node("Parque de los Venados_L12", pos=P("Parque de los Venados"), linea="L12", nombre="Parque de los Venados")
    G.add_node("Eje Central_L12", pos=P("Eje Central"), linea="L12", nombre="Eje Central")

    # Línea 1
    G.add_node("Observatorio_L1", pos=P("Observatorio"), linea="L1", nombre="Observatorio")
    G.add_node("Tacubaya_L1", pos=P("Tacubaya"), linea="L1", nombre="Tacubaya")
    G.add_node("Juanacatlan_L1", pos=P("Juanacatlan"), linea="L1", nombre="Juanacatlan")
    G.add_node("Chapultepec_L1", pos=P("Chapultepec"), linea="L1", nombre="Chapultepec")
    G.add_node("Sevilla_L1", pos=P("Sevilla"), linea="L1", nombre="Sevilla")
    G.add_node("Insurgentes_L1", pos=P("Insurgentes"), linea="L1", nombre="Insurgentes")
    G.add_node("Cuauhtemoc_L1", pos=P("Cuauhtemoc"), linea="L1", nombre="Cuauhtemoc")
    G.add_node("Balderas_L1", pos=P("Balderas"), linea="L1", nombre="Balderas")

    # ---------------------------------------------------------
    # 2. ARISTAS
    # ---------------------------------------------------------

    for (a,b),d in DISTANCIAS_REALES.items():
        # Tiempo = (Distancia / Velocidad) + Tiempo de parada en la estación
        tiempo_segundos = (d / VELOCIDAD_METRO) + TIEMPO_PARADA
        G.add_edge(a,b, weight=tiempo_segundos)

    # Tramos de transbordo
    TRANSBORDOS = [
        ("Tacubaya_L1", "Tacubaya_L7"),
        ("Tacubaya_L7", "Tacubaya_L9"), 
        ("Tacubaya_L1", "Tacubaya_L9"),
        ("Mixcoac_L7", "Mixcoac_L12"),
        ("Zapata_L3", "Zapata_L12"),
        ("Centro Medico_L3", "Centro Medico_L9"),
        ("Balderas_L1", "Balderas_L3")
    ]

    for origen, destino in TRANSBORDOS:
        G.add_edge(origen, destino, weight=PENALIZACION)

    # ---------------------------------------------------------
    # 3. SERVICIOS
    # ---------------------------------------------------------

    servicios_por_nodo = {
        # Línea 1
        "Observatorio_L1":      {"escalera": False, "ascensor": True},
        "Tacubaya_L1":          {"escalera": True,  "ascensor": True},
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
        "Tacubaya_L9":          {"escalera": True,  "ascensor": True},
        "Patriotismo_L9":       {"escalera": True,  "ascensor": False},
        "Chilpancingo_L9":      {"escalera": True,  "ascensor": False},
        "Centro Medico_L9":     {"escalera": True,  "ascensor": True},
        "Lazaro Cardenas_L9":   {"escalera": False, "ascensor": False},

        # Línea 7
        "Barranca del Muerto_L7":{"escalera": True, "ascensor": False},
        "Mixcoac_L7":           {"escalera": True,  "ascensor": True},
        "San Antonio_L7":       {"escalera": True,  "ascensor": False},
        "San Pedro de los Pinos_L7":{"escalera": True, "ascensor": False},
        "Tacubaya_L7":          {"escalera": True,  "ascensor": True},
        "Constituyentes_L7":    {"escalera": True,  "ascensor": False},
        "Auditorio_L7":         {"escalera": True,  "ascensor": False},
        "Polanco_L7":           {"escalera": True,  "ascensor": False},

        # Línea 3
        "Universidad_L3":       {"escalera": False, "ascensor": True},
        "Copilco_L3":           {"escalera": True,  "ascensor": True},
        "M.A. de Quevedo_L3":   {"escalera": True,  "ascensor": False},
        "Viveros_L3":           {"escalera": True,  "ascensor": False},
        "Coyoacan_L3":          {"escalera": False, "ascensor": False},
        "Zapata_L3":            {"escalera": True, "ascensor": True},
        "Division del Norte_L3":{"escalera": False, "ascensor": False},
        "Eugenia_L3":           {"escalera": False, "ascensor": False},
        "Etiopia_L3":           {"escalera": False, "ascensor": True},
        "Centro Medico_L3":     {"escalera": True,  "ascensor": True},
        "Hospital General_L3":  {"escalera": True,  "ascensor": True},
        "Ninos Heroes_L3":      {"escalera": False, "ascensor": False},
        "Balderas_L3":          {"escalera": True,  "ascensor": True},
        "Juarez_L3":            {"escalera": True,  "ascensor": True},
    }

    for node in G.nodes:
        datos = servicios_por_nodo.get(node, {"escalera": False, "ascensor": False})
        G.nodes[node]["escalera"] = datos["escalera"]
        G.nodes[node]["ascensor"] = datos["ascensor"]

    return G

# =============================================================
# INTERFAZ
# =============================================================
class AppMetro:
    def __init__(self,root):
        self.root=root
        self.root.title("Metro CDMX")
        self.root.resizable(True, True)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.graph = crear_grafo()
        self.nombres_estaciones = sorted(list({data["nombre"] for _,data in self.graph.nodes(data=True)}))

        # =========================================================
        # BARRA SUPERIOR
        # =========================================================
        self.frame_top = ctk.CTkFrame(root, height=65, fg_color="#F7F7F7", corner_radius=0)
        self.frame_top.pack(side="top", fill="x")

        self.card = ctk.CTkFrame(self.frame_top, fg_color="white",
                                 corner_radius=12, border_width=1,
                                 border_color="#DDDDDD")
        self.card.pack(padx=16, pady=10, fill="x")

        self.row = ctk.CTkFrame(self.card, fg_color="transparent")
        self.row.pack(padx=12, pady=8)
        self.row.pack_anchor = "center"

        # TÍTULO
        ctk.CTkLabel(self.row, text="Metro CDMX",
                     font=("Helvetica", 20, "bold"),
                     text_color="#222").pack(side="left", padx=20)

        # ORIGEN
        ctk.CTkLabel(self.row, text="Origen:", text_color="#555").pack(side="left")
        self.cb_origen = ctk.CTkComboBox(self.row, values=self.nombres_estaciones,
                                          width=150, height=32,
                                          corner_radius=10)
        self.cb_origen.pack(side="left", padx=10)

        # DESTINO
        ctk.CTkLabel(self.row, text="Destino:", text_color="#555").pack(side="left")
        self.cb_destino = ctk.CTkComboBox(self.row, values=self.nombres_estaciones,
                                          width=150, height=32,
                                          corner_radius=10)
        self.cb_destino.pack(side="left", padx=10)

        # CHECKBOXES
        self.var_escalera = ctk.BooleanVar()
        self.var_ascensor = ctk.BooleanVar()

        ctk.CTkCheckBox(self.row, text="Escaleras",
                        variable=self.var_escalera,
                        command=self.redibujar).pack(side="left", padx=5)

        ctk.CTkCheckBox(self.row, text="Ascensor",
                        variable=self.var_ascensor,
                        command=self.redibujar).pack(side="left", padx=5)

        # BOTÓN BUSCAR
        self.btn_buscar = ctk.CTkButton(self.row, text="Buscar Ruta",
                                        fg_color="#0078FF", hover_color="#0063D6",
                                        corner_radius=10,
                                        width=110,
                                        command=self.calcular)
        self.btn_buscar.pack(side="left", padx=20)

        # BOTÓN VOLVER
        self.btn_retroceder = ctk.CTkButton(
            self.row,
            text="Volver",
            fg_color="#E0E0E0",
            text_color="#222",
            hover_color="#C8C8C8",
            corner_radius=10,
            width=80,
            command=self.retroceder
        )

        self.btn_retroceder.pack(side="left", padx=(10, 0))

        # Estado inicial invisible
        self.btn_retroceder.configure(state="disabled", fg_color="transparent", text="")

        # INFO EN LA BARRA
        self.lbl = ctk.CTkLabel(self.row, text="", text_color="#333")
        self.lbl.pack(side="left", padx=10)

        # =========================================================
        # PANEL DERECHO (MAPA)
        # =========================================================
        self.frame_right=tk.Frame(root)
        self.frame_right.pack(side="right", fill="both", expand=True)

        self.canvas=tk.Canvas(self.frame_right, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.img_pil = Image.open("Mapa_metro.png")
        self.orig_w, self.orig_h = self.img_pil.size
        
        # Iconos de servicios
        try:
            # Cargar icono de escalera
            img_esc_pil = Image.open("escalera.png")
            img_esc_resized = img_esc_pil.resize((14, 14), Image.LANCZOS)
            self.icon_escalera_tk = ImageTk.PhotoImage(img_esc_resized)

            # Cargar icono de ascensor
            img_asc_pil = Image.open("ascensor.png")
            img_asc_resized = img_asc_pil.resize((14, 14), Image.LANCZOS)
            self.icon_ascensor_tk = ImageTk.PhotoImage(img_asc_resized)

        except Exception as e:
            print(f"Error cargando íconos: {e}")
            self.icon_escalera_tk = None
            self.icon_ascensor_tk = None
            
        self.canvas.bind("<Configure>", lambda e:self.redibujar())

        # =========================================================
        # PANEL DE INFORMACIÓN FLOTANTE SOBRE EL MAPA
        # =========================================================
        self.info_panel = ctk.CTkFrame(
            self.frame_right,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#DDDDDD"
        )
        self.info_panel.place(relx=0.98, rely=0.05, anchor="ne")

        self.info_title = ctk.CTkLabel(
            self.info_panel,
            text="Información de Ruta",
            font=("Helvetica", 16, "bold"),
            text_color="#333"
        )
        self.info_title.pack(padx=10, pady=(10,5))

        self.info_text = ctk.CTkLabel(
            self.info_panel,
            text="Selecciona estaciones...",
            justify="left",
            font=("Helvetica", 13),
            text_color="#444"
        )
        self.info_text.pack(padx=10, pady=(0,10))

        self.ruta=None
        self.nodo_origen_click=None
        self.nodo_destino_click=None

    # ============================================================
    # REDIBUJAR
    # ============================================================
    def redibujar(self):
        self.canvas.delete("all")

        # 1. Fondo (BN si se ha calculado ruta, es decir, si se ha pulsado buscar)
        if self.ruta:
            imagen_a_cargar = "Mapa_metro_BN.png"
        else:
            imagen_a_cargar = "Mapa_metro.png"

        try:
            self.img_pil = Image.open(imagen_a_cargar)
        except:
            return

        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()

        self.scale = min(cw / self.orig_w, ch / self.orig_h)
        nw, nh = int(self.orig_w * self.scale), int(self.orig_h * self.scale)
        self.ox = (cw - nw) // 2
        self.oy = (ch - nh) // 2

        img = self.img_pil.resize((nw, nh), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)

        self.canvas.create_image(cw // 2, ch // 2, image=self.tk_img)

        # 2. Iconos de servicios
        mostrar_escalera = self.var_escalera.get() and self.icon_escalera_tk
        mostrar_ascensor = self.var_ascensor.get() and self.icon_ascensor_tk

        # Conjunto para recordar qué nombres de estación ya se ha procesado
        estaciones_dibujadas = set()

        if mostrar_escalera or mostrar_ascensor:
            # Ordenamos para asegurar consistencia al dibujar
            for n, data in sorted(self.graph.nodes(data=True)):
                nombre_real = data["nombre"]

                # Si ya se ha dibujado iconos para una estación se salta las variantes (L1, L7, etc.)
                if nombre_real in estaciones_dibujadas:
                    continue

                tiene_escalera = data.get("escalera", False)
                tiene_ascensor = data.get("ascensor", False)

                if not (mostrar_escalera and tiene_escalera) and not (mostrar_ascensor and tiene_ascensor):
                    continue

                # Se marca la estación como "ya dibujada"
                estaciones_dibujadas.add(nombre_real)

                x, y = data["pos"]
                X, Y = self.convertir(x, y)
                base_icon_x = X - 15
                base_icon_y = Y - 15
                
                offset_incremental = 0 
                if mostrar_escalera and tiene_escalera:
                    self.canvas.create_image(
                        base_icon_x + offset_incremental, 
                        base_icon_y,
                        image=self.icon_escalera_tk,
                        anchor="center"
                    )
                    offset_incremental += 20 

                if mostrar_ascensor and tiene_ascensor:
                    self.canvas.create_image(
                        base_icon_x + offset_incremental, 
                        base_icon_y,
                        image=self.icon_ascensor_tk,
                        anchor="center"
                    )

        # 3. Zonas clicables
        self.node_items = {}
        for node, data in self.graph.nodes(data=True):
            x, y = data["pos"]
            X, Y = self.convertir(x, y)
            r = 12
            item = self.canvas.create_oval(X - r, Y - r, X + r, Y + r, fill="", outline="", width=0)
            self.node_items[node] = item
            self.canvas.tag_bind(item, "<Button-1>", lambda e, n=node: self.on_node_click(n))

        # 4. Marcadores de selección
        if self.nodo_origen_click:
            x, y = self.graph.nodes[self.nodo_origen_click]["pos"]
            X, Y = self.convertir(x, y)
            self.canvas.create_oval(X - 14, Y - 14, X + 14, Y + 14, outline="#39FF14", width=6)

        if self.nodo_destino_click:
            x, y = self.graph.nodes[self.nodo_destino_click]["pos"]
            X, Y = self.convertir(x, y)
            self.canvas.create_oval(X - 14, Y - 14, X + 14, Y + 14, outline="red", width=6)

        # 5. Ruta
        if self.ruta:
            self.dibujar_ruta()

    def convertir(self,x,y):
        return (x*self.scale + self.ox, y*self.scale + self.oy)

    # ============================================================
    # CLIC
    # ============================================================
    def on_node_click(self,node):
        nombre = self.graph.nodes[node]["nombre"]

        if self.nodo_origen_click is None:
            self.nodo_origen_click=node
            self.cb_origen.set(nombre)

        elif self.nodo_destino_click is None:
            if node!=self.nodo_origen_click:
                self.nodo_destino_click=node
                self.cb_destino.set(nombre)

        else:
            self.nodo_origen_click=node
            self.nodo_destino_click=None
            self.cb_origen.set(nombre)
            self.cb_destino.set("")

        self.info_text.configure(text=f"Seleccionada: {nombre}")

        self.redibujar()

    # ============================================================
    # RETROCEDER
    # ============================================================
    def retroceder(self):
        self.ruta=None
        self.nodo_origen_click=None
        self.nodo_destino_click=None
        self.cb_origen.set("")
        self.cb_destino.set("")
        self.info_text.configure(text="Selecciona estaciones...")
        self.redibujar()
        self.btn_retroceder.configure(state="disabled", fg_color="transparent", text="")

    # ============================================================
    # CALCULAR RUTA
    # ============================================================
    def get_node_id(self, nombre):
        for n,data in self.graph.nodes(data=True):
            if data["nombre"]==nombre:
                return n
        return None
    
    def contar_transbordos(self, ruta):
        contador = 0
        for i in range(len(ruta) - 1):
            nodo_actual = ruta[i]
            nodo_siguiente = ruta[i+1]
            
            linea_a = self.graph.nodes[nodo_actual]["linea"]
            linea_b = self.graph.nodes[nodo_siguiente]["linea"]
            
            # Si las líneas son diferentes, es un transbordo
            if linea_a != linea_b:
                contador += 1
        return contador
    
    def es_transbordo_inicial(self, ruta):
        if len(ruta) < 2:
            return False  # No hay suficientes nodos para formar un transbordo
        
        primer_nodo = ruta[0]
        segundo_nodo = ruta[1]
        
        linea_primer = self.graph.nodes[primer_nodo]["linea"]
        linea_segundo = self.graph.nodes[segundo_nodo]["linea"]
        
        # Si las líneas son diferentes, es un transbordo
        return linea_primer != linea_segundo

    def calcular(self):
        o = self.cb_origen.get()
        d = self.cb_destino.get()

        if not o or not d:
            messagebox.showwarning("Error", "Selecciona origen y destino")
            return

        so = self.get_node_id(o)
        sd = self.get_node_id(d)
        
        if so is None or sd is None:
            messagebox.showwarning("Error", "No se encontraron las estaciones en el grafo.")
            return

        # VALIDACION SOLO EN ORIGEN Y DESTINO
        if self.var_escalera.get() and not self.graph.nodes[so].get("escalera", False):
            messagebox.showwarning("Accesibilidad", "La estación de origen no dispone de escaleras.")
            return
        if self.var_ascensor.get() and not self.graph.nodes[so].get("ascensor", False):
            messagebox.showwarning("Accesibilidad", "La estación de origen no dispone de ascensor.")
            return

        if self.var_escalera.get() and not self.graph.nodes[sd].get("escalera", False):
            messagebox.showwarning("Accesibilidad", "La estación de destino no dispone de escaleras.")
            return
        if self.var_ascensor.get() and not self.graph.nodes[sd].get("ascensor", False):
            messagebox.showwarning("Accesibilidad", "La estación de destino no dispone de ascensor.")
            return

        ruta, tiempo = astar_path(self.graph, so, sd)

        if not ruta:
            messagebox.showerror("Sin ruta", "No hay ruta posible.")
            return

        self.ruta = ruta
        
        # --- CÁLCULO DE ESTADÍSTICAS ---
        num_transbordos = self.contar_transbordos(ruta)
        # Restamos los transbordos y el nodo inicial para tener el n° de estaciones viajadas real
        num_estaciones = len(ruta) - 1 - num_transbordos
        tiempo_minutos = math.ceil(tiempo / 60)
        if self.es_transbordo_inicial(ruta): 
            num_transbordos -= 1

        self.info_text.configure(
            text=f"Tiempo: {tiempo_minutos} min\n"
                 f"Estaciones: {num_estaciones}\n"
                 f"Transbordos: {num_transbordos}"
        )

        self.btn_retroceder.configure(state="normal", fg_color="#E0E0E0", text="Volver")
        self.redibujar()

    # ============================================================
    # DIBUJAR RUTA
    # ============================================================
    def dibujar_ruta(self):
        # 1. LÍNEAS
        for a, b in zip(self.ruta, self.ruta[1:]):
            x1, y1 = self.graph.nodes[a]["pos"]
            x2, y2 = self.graph.nodes[b]["pos"]
            X1, Y1 = self.convertir(x1, y1)
            X2, Y2 = self.convertir(x2, y2)
            # Línea cian gruesa
            self.canvas.create_line(X1, Y1, X2, Y2, fill="cyan", width=6)

        # 2. NODOS INTERMEDIOS
        for estacion in self.ruta[1:-1]:
            x, y = self.graph.nodes[estacion]["pos"]
            X, Y = self.convertir(x, y)
            
            # Círculo blanco pequeño (4 pixeles de radio)
            self.canvas.create_oval(X-4, Y-4, X+4, Y+4, fill="white", outline="black", width=1)

        # 3. INICIO (Verde)
        a = self.ruta[0]
        x, y = self.graph.nodes[a]["pos"]
        X, Y = self.convertir(x, y)
        self.canvas.create_oval(X-10, Y-10, X+10, Y+10, fill="#39FF14", outline="black", width=3)

        # 4. FIN (Rojo)
        b = self.ruta[-1]
        x, y = self.graph.nodes[b]["pos"]
        X, Y = self.convertir(x, y)
        self.canvas.create_oval(X-10, Y-10, X+10, Y+10, fill="#FF3333", outline="black", width=3)


# =============================================================
# EJECUTAR
# =============================================================

if __name__=="__main__":
    root=ctk.CTk()
    root.geometry("1400x900")
    AppMetro(root)
    root.mainloop()