import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import networkx as nx
import math
import heapq

# =============================================================
# 0. CONSTANTES DEL SEGUNDO CÓDIGO
# =============================================================

PENALIZACION = 5
VELOCIDAD_METRO = 10.0  # m/s

# ---- HEURÍSTICA (lat/lon del segundo código) ----
HEURISTICA = {
    # Línea 1
    "Observatorio_L1": (19.398333, -99.200278),
    "Tacubaya_L1": (19.403333, -99.187222),
    "Juanacatlan_L1": (19.412778, -99.182222),
    "Chapultepec_L1": (19.420833, -99.176389),
    "Sevilla_L1": (19.421944, -99.170556),
    "Insurgentes_L1": (19.423333, -99.163056),
    "Cuauhtemoc_L1": (19.425833, -99.154722),
    "Balderas_L1": (19.427500, -99.149167),

    # Línea 12
    "Mixcoac_L12": (19.375833, -99.187500),
    "Insurgentes Sur_L12": (19.373611, -99.178889),
    "Hospital 20 de Nov_L12": (19.371944, -99.171111),
    "Zapata_L12": (19.370833, -99.165000),
    "Parque de los Venados_L12": (19.370833, -99.158611),
    "Eje Central_L12": (19.361389, -99.151389),

    # Línea 9
    "Tacubaya_L9": (19.403333, -99.187222),
    "Patriotismo_L9": (19.406111, -99.178889),
    "Chilpancingo_L9": (19.405833, -99.168611),
    "Centro Medico_L9": (19.406667, -99.155833),
    "Lazaro Cardenas_L9": (19.406944, -99.145000),

    # Línea 7
    "Barranca del Muerto_L7": (19.360556, -99.190278),
    "Mixcoac_L7": (19.375833, -99.187500),
    "San Antonio_L7": (19.384722, -99.186389),
    "San Pedro de los Pinos_L7": (19.391389, -99.186111),
    "Tacubaya_L7": (19.403333, -99.187222),
    "Constituyentes_L7": (19.411944, -99.191389),
    "Auditorio_L7": (19.425556, -99.191944),
    "Polanco_L7": (19.433611, -99.191111),

    # Línea 3
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

# ---- Distancias del segundo código ----
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
# 1. FUNCIONES A*
# =============================================================

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2-lat1)
    dlambda = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

def heuristica(graph, a, b):
    lat1, lon1 = HEURISTICA[a]
    lat2, lon2 = HEURISTICA[b]
    dist = haversine(lat1, lon1, lat2, lon2)
    return dist / VELOCIDAD_METRO

def get_dist(a, b):
    if (a,b) in DISTANCIAS_REALES:
        return DISTANCIAS_REALES[(a,b)]
    if (b,a) in DISTANCIAS_REALES:
        return DISTANCIAS_REALES[(b,a)]
    return 1000

def buscar_ruta(graph, start, end, esc=False, asc=False):
    open_set=[]
    heapq.heappush(open_set,(0,start))
    g={n:float("inf") for n in graph.nodes}
    g[start]=0
    f={n:float("inf") for n in graph.nodes}
    f[start]=heuristica(graph,start,end)
    came={}

    while open_set:
        _,current=heapq.heappop(open_set)

        if current==end:
            ruta=[]
            while current in came:
                ruta.append(current)
                current=came[current]
            ruta.append(start)
            ruta.reverse()
            return ruta, g[end]

        for nb in graph.neighbors(current):

            # accesibilidad SOLO si hay transbordo:
            if graph.nodes[current]["linea"]!=graph.nodes[nb]["linea"]:
                if esc and not (graph.nodes[current]["escalera"] and graph.nodes[nb]["escalera"]):
                    continue
                if asc and not (graph.nodes[current]["ascensor"] and graph.nodes[nb]["ascensor"]):
                    continue

            peso = graph[current][nb]["weight"]
            ng = g[current] + peso

            if ng < g[nb]:
                g[nb]=ng
                came[nb]=current
                f[nb]=ng + heuristica(graph,nb,end)
                heapq.heappush(open_set,(f[nb],nb))

    return None,0

# =============================================================
# 2. GRAFO: POSICIONES DEL SEGUNDO CÓDIGO + SERVICIOS
# =============================================================

import json
import os

def crear_grafo():
    G = nx.Graph()

    # --- 1. Cargar JSON ---
    with open("coordenadas_metro.json", "r") as f:
        coords = json.load(f)

    # --- 2. Función helper ---
    def get_pos(nombre):
        if nombre in coords:
            return coords[nombre]
        print("⚠ Pos no encontrada en JSON:", nombre)
        return (0,0)

    # ---------------------------
    #  NODOS (igual que antes)
    #  PERO usando pos=get_pos(...)
    # ---------------------------

    # Línea 7
    G.add_node("Polanco_L7", pos=get_pos("Polanco"), linea="L7", nombre="Polanco")
    G.add_node("Auditorio_L7", pos=get_pos("Auditorio"), linea="L7", nombre="Auditorio")
    G.add_node("Constituyentes_L7", pos=get_pos("Constituyentes"), linea="L7", nombre="Constituyentes")
    G.add_node("Tacubaya_L7", pos=get_pos("Tacubaya"), linea="L7", nombre="Tacubaya")
    G.add_node("San Pedro de los Pinos_L7", pos=get_pos("San Pedro de los Pinos"), linea="L7", nombre="San Pedro de los Pinos")
    G.add_node("San Antonio_L7", pos=get_pos("San Antonio"), linea="L7", nombre="San Antonio")
    G.add_node("Mixcoac_L7", pos=get_pos("Mixcoac"), linea="L7", nombre="Mixcoac")
    G.add_node("Barranca del Muerto_L7", pos=get_pos("Barranca del Muerto"), linea="L7", nombre="Barranca del Muerto")

    # Línea 3
    G.add_node("Juarez_L3", pos=get_pos("Juarez"), linea="L3", nombre="Juarez")
    G.add_node("Balderas_L3", pos=get_pos("Balderas"), linea="L3", nombre="Balderas")
    G.add_node("Ninos Heroes_L3", pos=get_pos("Ninos Heroes"), linea="L3", nombre="Ninos Heroes")
    G.add_node("Hospital General_L3", pos=get_pos("Hospital General"), linea="L3", nombre="Hospital General")
    G.add_node("Centro Medico_L3", pos=get_pos("Centro Medico"), linea="L3", nombre="Centro Medico")
    G.add_node("Etiopia_L3", pos=get_pos("Etiopia"), linea="L3", nombre="Etiopia")
    G.add_node("Eugenia_L3", pos=get_pos("Eugenia"), linea="L3", nombre="Eugenia")
    G.add_node("Division del Norte_L3", pos=get_pos("Division del Norte"), linea="L3", nombre="Division del Norte")
    G.add_node("Zapata_L3", pos=get_pos("Zapata"), linea="L3", nombre="Zapata")
    G.add_node("Coyoacan_L3", pos=get_pos("Coyoacan"), linea="L3", nombre="Coyoacan")
    G.add_node("Viveros_L3", pos=get_pos("Viveros"), linea="L3", nombre="Viveros")
    G.add_node("M.A. de Quevedo_L3", pos=get_pos("M.A. de Quevedo"), linea="L3", nombre="M.A. de Quevedo")
    G.add_node("Copilco_L3", pos=get_pos("Copilco"), linea="L3", nombre="Copilco")
    G.add_node("Universidad_L3", pos=get_pos("Universidad"), linea="L3", nombre="Universidad")

    # Línea 9
    G.add_node("Tacubaya_L9", pos=get_pos("Tacubaya"), linea="L9", nombre="Tacubaya")
    G.add_node("Patriotismo_L9", pos=get_pos("Patriotismo"), linea="L9", nombre="Patriotismo")
    G.add_node("Chilpancingo_L9", pos=get_pos("Chilpancingo"), linea="L9", nombre="Chilpancingo")
    G.add_node("Centro Medico_L9", pos=get_pos("Centro Medico"), linea="L9", nombre="Centro Medico")
    G.add_node("Lazaro Cardenas_L9", pos=get_pos("Lazaro Cardenas"), linea="L9", nombre="Lazaro Cardenas")

    # Línea 12
    G.add_node("Mixcoac_L12", pos=get_pos("Mixcoac"), linea="L12", nombre="Mixcoac")
    G.add_node("Insurgentes Sur_L12", pos=get_pos("Insurgentes Sur"), linea="L12", nombre="Insurgentes Sur")
    G.add_node("Hospital 20 de Nov_L12", pos=get_pos("Hospital 20 de Nov"), linea="L12", nombre="Hospital 20 de Nov")
    G.add_node("Zapata_L12", pos=get_pos("Zapata"), linea="L12", nombre="Zapata")
    G.add_node("Parque de los Venados_L12", pos=get_pos("Parque de los Venados"), linea="L12", nombre="Parque de los Venados")
    G.add_node("Eje Central_L12", pos=get_pos("Eje Central"), linea="L12", nombre="Eje Central")

    # Línea 1
    G.add_node("Observatorio_L1", pos=get_pos("Observatorio"), linea="L1", nombre="Observatorio")
    G.add_node("Tacubaya_L1", pos=get_pos("Tacubaya"), linea="L1", nombre="Tacubaya")
    G.add_node("Juanacatlan_L1", pos=get_pos("Juanacatlan"), linea="L1", nombre="Juanacatlan")
    G.add_node("Chapultepec_L1", pos=get_pos("Chapultepec"), linea="L1", nombre="Chapultepec")
    G.add_node("Sevilla_L1", pos=get_pos("Sevilla"), linea="L1", nombre="Sevilla")
    G.add_node("Insurgentes_L1", pos=get_pos("Insurgentes"), linea="L1", nombre="Insurgentes")
    G.add_node("Cuauhtemoc_L1", pos=get_pos("Cuauhtemoc"), linea="L1", nombre="Cuauhtemoc")
    G.add_node("Balderas_L1", pos=get_pos("Balderas"), linea="L1", nombre="Balderas")

    # ARISTAS IGUAL QUE ANTES…
    for (a,b), dist in DISTANCIAS_REALES.items():
        G.add_edge(a,b,weight=dist/VELOCIDAD_METRO)

    # TRANSBORDOS
    G.add_edge("Tacubaya_L1","Tacubaya_L7", weight=PENALIZACION)
    G.add_edge("Tacubaya_L7","Tacubaya_L9", weight=PENALIZACION)
    G.add_edge("Mixcoac_L7","Mixcoac_L12", weight=PENALIZACION)
    G.add_edge("Zapata_L3","Zapata_L12", weight=PENALIZACION)
    G.add_edge("Centro Medico_L3","Centro Medico_L9", weight=PENALIZACION)
    G.add_edge("Balderas_L1","Balderas_L3", weight=PENALIZACION)

    # Servicios
    for n in G.nodes:
        G.nodes[n]["escalera"] = True
        G.nodes[n]["ascensor"] = True

    return G


# =============================================================
# 3. INTERFAZ → Basada en la del primer código
# =============================================================

class AppMetro:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro CDMX - A* + Mapa")

        self.graph = crear_grafo()

        self.nombres_estaciones = sorted(list({
            data["nombre"] for n,data in self.graph.nodes(data=True)
        }))

        # panel izquierdo
        self.frame_left = tk.Frame(root, width=250, bg="#f5f5f5")
        self.frame_left.pack(side="left", fill="y")
        self.frame_left.pack_propagate(False)


        tk.Label(self.frame_left, text="Metro CDMX", font=("Helvetica",20,"bold"),
                 bg="#f5f5f5").pack(pady=20)

        tk.Label(self.frame_left, text="Origen:", bg="#f5f5f5").pack(anchor="w")
        self.cb_origen = ttk.Combobox(self.frame_left, values=self.nombres_estaciones)
        self.cb_origen.pack(fill="x")

        tk.Label(self.frame_left, text="Destino:", bg="#f5f5f5").pack(anchor="w", pady=10)
        self.cb_destino = ttk.Combobox(self.frame_left, values=self.nombres_estaciones)
        self.cb_destino.pack(fill="x")

        self.var_escal = tk.BooleanVar()
        self.var_ascen = tk.BooleanVar()

        tk.Checkbutton(self.frame_left, text="Requiere escaleras",
                       variable=self.var_escal, bg="#f5f5f5").pack(anchor="w")
        tk.Checkbutton(self.frame_left, text="Requiere ascensor",
                       variable=self.var_ascen, bg="#f5f5f5").pack(anchor="w")

        tk.Button(self.frame_left,text="Buscar Ruta",bg="#007aff",fg="white",
                  command=self.calcular).pack(fill="x", pady=20)
        self.btn_retroceder = tk.Button(self.frame_left, text="Retroceder",bg="#888", fg="white",command=self.retroceder)
# NO lo empaques aún → queda oculto



        self.lbl = tk.Label(self.frame_left, text="", bg="#f5f5f5", justify="left")
        self.lbl.pack(anchor="w")

        # panel derecho (canvas con imagen)
        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame_right, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.cargar_imagen("Mapa_metro.png")

        self.canvas.bind("<Configure>", lambda e:self.redibujar())

        self.ruta = None
        self.nodo_clickado = None
        self.nodo_origen_click = None
        self.nodo_destino_click = None



    def cargar_imagen(self,path):
        self.img_pil = Image.open(path)
        self.orig_w, self.orig_h = self.img_pil.size
        self.redibujar()

    def redibujar(self):
        # ====== MODO ESCALERAS ======
        if self.var_escal.get() and not self.ruta:
        # cargar blanco y negro
            try:
                self.img_pil = Image.open("Mapa_metro_BN.png")
            except:
                print("⚠ No se encontró Mapa_metro_BN.png")
        else:
    # cargar mapa normal
            try:

                self.img_pil = Image.open("Mapa_metro.png")
            except:
                print("⚠ No se encontró Mapa_metro.png")

        self.canvas.delete("all")

        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()

        if cw < 10 or ch < 10:
            return

    # --- escalar imagen ---
        scale = min(cw/self.orig_w, ch/self.orig_h)
        nw, nh = int(self.orig_w * scale), int(self.orig_h * scale)
        ox, oy = (cw-nw)//2, (ch-nh)//2

        self.scale, self.ox, self.oy = scale, ox, oy

        img = self.img_pil.resize((nw, nh), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(cw//2, ch//2, image=self.tk_img)

    # ====== 🔥 CREAR NODOS CLICABLES SIEMPRE ======
        self.node_items = {}

        for node, data in self.graph.nodes(data=True):
            x, y = data["pos"]
            X, Y = self.convertir(x, y)

            r = 14  # área clicable

            item = self.canvas.create_oval(
                X - r, Y - r, X + r, Y + r,
                fill="", outline="", width=0,  # invisibles
                tags=("nodo")
        )

            self.node_items[node] = item

        # Bind del clic
            self.canvas.tag_bind(
                item,
                "<Button-1>",
                lambda e, n=node: self.on_node_click(n)
            )
                # ====== ORIGEN SELECCIONADO (VERDE) ======
        if self.nodo_origen_click:
            x, y = self.graph.nodes[self.nodo_origen_click]["pos"]
            X, Y = self.convertir(x, y)
            self.canvas.create_oval(
                X-14, Y-14, X+14, Y+14,
                outline="#00FF00", width=4
            )
            self.canvas.create_oval(
                X-8, Y-8, X+8, Y+8,
                fill="#32CD32", outline="black", width=2
            )

        # ====== DESTINO SELECCIONADO (ROJO) ======
        if self.nodo_destino_click:
            x, y = self.graph.nodes[self.nodo_destino_click]["pos"]
            X, Y = self.convertir(x, y)
            self.canvas.create_oval(
                X-14, Y-14, X+14, Y+14,
                outline="#FF0000", width=4
            )
            self.canvas.create_oval(
                X-8, Y-8, X+8, Y+8,
                fill="#FF4444", outline="black", width=2
            )

   
        # ====== NODOS ACCESSIBLES POR ESCALERA ======
        if self.var_escal.get() and not self.ruta:
            for node, data in self.graph.nodes(data=True):
                if data["escalera"]:
                    x, y = data["pos"]
                    X, Y = self.convertir(x, y)

                    self.canvas.create_oval(
                        X-10, Y-10, X+10, Y+10,
                        outline="gold", width=4
                    )
                    self.canvas.create_oval(
                        X-6, Y-6, X+6, Y+6,
                        fill="yellow", outline="black", width=2
                    )



        # ====== RUTA (si existe) ======
        if self.ruta:
            self.dibujar_ruta()



    



    def convertir(self,x,y):
        return (x*self.scale + self.ox, y*self.scale + self.oy)

    def get_node_id(self, nombre):
        for n,data in self.graph.nodes(data=True):
            if data["nombre"]==nombre:
                return n
        return None
    
    def retroceder(self):
        if not self.ruta:
            return

        self.ruta = None
        self.nodo_origen_click = None
        self.nodo_destino_click = None
        self.cb_origen.set("")
        self.cb_destino.set("")


        try:
            self.cargar_imagen("Mapa_metro.png")
        except:
            print("⚠ No se encontró Mapa_metro.png")

        self.lbl.config(text="")
        self.redibujar()

        # Ocultar botón
        self.btn_retroceder.pack_forget()




    def calcular(self):
        o = self.cb_origen.get()
        d = self.cb_destino.get()
        if not o or not d:
            messagebox.showwarning("Error", "Selecciona origen y destino")
            return

        so = self.get_node_id(o)
        sd = self.get_node_id(d)

        ruta, tiempo = buscar_ruta(
            self.graph, so, sd,
            self.var_escal.get(),
            self.var_ascen.get()
        )

        if not ruta:
            messagebox.showerror("Sin ruta", "No hay ruta posible.")
            return

        # --- Guardar ruta
        self.ruta = ruta
        self.lbl.config(
            text=f"Tiempo: {math.ceil(tiempo/60)} min\nEstaciones: {len(ruta)}"
        )

        # BOTON retroceder
        self.btn_retroceder.pack(fill="x", pady=5)


        # --- 🔥 Cambiar mapa a BN
        try:
            self.cargar_imagen("Mapa_metro_BN.png")
        except:
            print("⚠ No se encontró Mapa_metro_BN.png, usando el mapa normal.")
        self.redibujar()

        # --- Forzar redibujo con la nueva imagen + ruta
        self.redibujar()


    def dibujar_ruta(self):
        # --- Lineas entre estaciones ---
        for i in range(len(self.ruta)-1):
            a = self.ruta[i]
            b = self.ruta[i+1]
            x1,y1 = self.graph.nodes[a]["pos"]
            x2,y2 = self.graph.nodes[b]["pos"]
            X1,Y1 = self.convertir(x1,y1)
            X2,Y2 = self.convertir(x2,y2)
            self.canvas.create_line(
                X1, Y1, X2, Y2,
                fill="cyan", width=8, tags="ruta"
            )

        # --- Nodos intermedios (rojo) ---
        for n in self.ruta[1:-1]:
            x, y = self.graph.nodes[n]["pos"]
            X, Y = self.convertir(x, y)
            self.canvas.create_oval(
                X-5, Y-5, X+5, Y+5,
                fill="white", outline="white", width=2, tags="ruta"
            )

        # --- Nodo INICIO (amarillo) ---
        n_ini = self.ruta[0]
        x, y = self.graph.nodes[n_ini]["pos"]
        X, Y = self.convertir(x, y)
        self.canvas.create_oval(
            X-10, Y-10, X+10, Y+10,   # un poco más grande
            fill="LawnGreen", outline="black", width=3, tags="ruta"
        )

        # --- Nodo FIN (amarillo) ---
        n_fin = self.ruta[-1]
        x, y = self.graph.nodes[n_fin]["pos"]
        X, Y = self.convertir(x, y)
        self.canvas.create_oval(
            X-10, Y-10, X+10, Y+10,
            fill="red", outline="black", width=3, tags="ruta"
        )


    def on_node_click(self, node_id):
        nombre = self.graph.nodes[node_id]["nombre"]

        # --- Selección ORIGEN / DESTINO ---
        if self.nodo_origen_click is None:
            # Primer clic → ORIGEN
            self.nodo_origen_click = node_id
            self.cb_origen.set(nombre)

        elif self.nodo_destino_click is None:
            # Segundo clic → DESTINO (y que no sea igual al origen)
            if node_id != self.nodo_origen_click:
                self.nodo_destino_click = node_id
                self.cb_destino.set(nombre)

        else:
            # Si ya había origen y destino → reiniciar
            self.nodo_origen_click = node_id
            self.nodo_destino_click = None
            self.cb_origen.set(nombre)
            self.cb_destino.set("")

        # Mostrar nombre
        self.lbl.config(text=f"Seleccionada: {nombre}")

        # Redibujar marcadores
        self.redibujar()



    

# -------------------------------------------------------------

if __name__=="__main__":
    root = tk.Tk()
    root.geometry("1100x900")
    AppMetro(root)
    root.mainloop()
