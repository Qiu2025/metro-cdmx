import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import networkx as nx
import math
import heapq

# ============================================================================
# 0. DATOS Y METODOS AUXILIARES
# ============================================================================

# Penalizacion de los transbordos
PENALIZACION = 5 * 60    # 5 minutos
TIEMPO_PARADA = 20       # segundos

# Velocidad media del metro: 36 km/h = 10 m/s
VELOCIDAD_METRO = 10.0  # m/s

# Latitudes y altitudes obtenidos de wikipedia, es la h(n)
HEURISTICA = {
    # Línea 1 (L1)
    "Observatorio_L1": (19.398333, -99.200278),
    "Tacubaya_L1": (19.403333, -99.187222),
    "Juanacatlan_L1": (19.412778, -99.182222),
    "Chapultepec_L1": (19.420833, -99.176389),
    "Sevilla_L1": (19.421944, -99.170556),
    "Insurgentes_L1": (19.423333, -99.163056),
    "Cuauhtemoc_L1": (19.425833, -99.154722),
    "Balderas_L1": (19.427500, -99.149167),
    
    # Línea 12 (L12)
    "Mixcoac_L12": (19.375833, -99.187500),
    "Insurgentes Sur_L12": (19.373611, -99.178889),
    "Hospital 20 de Nov_L12": (19.371944, -99.171111),
    "Zapata_L12": (19.370833, -99.165000),
    "Parque de los Venados_L12": (19.370833, -99.158611),
    "Eje Central_L12": (19.361389, -99.151389),
    
    # Línea 9 (L9)
    "Tacubaya_L9": (19.403333, -99.187222),
    "Patriotismo_L9": (19.406111, -99.178889),
    "Chilpancingo_L9": (19.405833, -99.168611),
    "Centro Medico_L9": (19.406667, -99.155833),
    "Lazaro Cardenas_L9": (19.406944, -99.145000),
    
    # Línea 7 (L7)
    "Barranca del Muerto_L7": (19.360556, -99.190278),
    "Mixcoac_L7": (19.375833, -99.187500),
    "San Antonio_L7": (19.384722, -99.186389),
    "San Pedro de los Pinos_L7": (19.391389, -99.186111),
    "Tacubaya_L7": (19.403333, -99.187222),
    "Constituyentes_L7": (19.411944, -99.191389),
    "Auditorio_L7": (19.425556, -99.191944),
    "Polanco_L7": (19.433611, -99.191111),
    
    # Línea 3 (L3)
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

# Distancias reales entre estaciones (una y la siguiente) en metros, es la g(n)
DISTANCIAS_REALES = {
    # LINEA 1
    ("Observatorio_L1", "Tacubaya_L1"): 1262,
    ("Tacubaya_L1", "Juanacatlan_L1"): 1158,
    ("Juanacatlan_L1", "Chapultepec_L1"): 973,
    ("Chapultepec_L1", "Sevilla_L1"): 501,
    ("Sevilla_L1", "Insurgentes_L1"): 645,
    ("Insurgentes_L1", "Cuauhtemoc_L1"): 793,
    ("Cuauhtemoc_L1", "Balderas_L1"): 409,

    # LINEA 12
    ("Mixcoac_L12", "Insurgentes Sur_L12"): 651,
    ("Insurgentes Sur_L12", "Hospital 20 de Nov_L12"): 725,
    ("Hospital 20 de Nov_L12", "Zapata_L12"): 450,
    ("Zapata_L12", "Parque de los Venados_L12"): 563,
    ("Parque de los Venados_L12", "Eje Central_L12"): 1280,

    # LINEA 9
    ("Tacubaya_L9", "Patriotismo_L9"): 1133,
    ("Patriotismo_L9", "Chilpancingo_L9"): 955,
    ("Chilpancingo_L9", "Centro Medico_L9"): 1152,
    ("Centro Medico_L9", "Lazaro Cardenas_L9"): 1059,

    # LINEA 7
    ("Barranca del Muerto_L7", "Mixcoac_L7"): 1476,
    ("Mixcoac_L7", "San Antonio_L7"): 788,
    ("San Antonio_L7", "San Pedro de los Pinos_L7"): 606,
    ("San Pedro de los Pinos_L7", "Tacubaya_L7"): 1084,
    ("Tacubaya_L7", "Constituyentes_L7"): 1005,
    ("Constituyentes_L7", "Auditorio_L7"): 1430,
    ("Auditorio_L7", "Polanco_L7"): 812,

    # LINEA 3
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

# Metodos auxiliares
def get_dist(a, b):
    """Devuelve la distancia en metros entre dos estaciones consecutivas."""
    if (a, b) in DISTANCIAS_REALES:
        return DISTANCIAS_REALES[(a, b)]
    if (b, a) in DISTANCIAS_REALES:
        return DISTANCIAS_REALES[(b, a)]
    raise KeyError(f"No se encontró distancia para el tramo {a} - {b}")

def add_tramo(metro, a, b):
    """Añade un tramo con peso = tiempo en segundos (distancia / velocidad)."""
    dist_m = get_dist(a, b)
    tiempo_seg = dist_m / VELOCIDAD_METRO
    metro.add_edge(a, b, weight=tiempo_seg + TIEMPO_PARADA)

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

def añadir_aristas_transbordo(metro):
    for origen, destino in TRANSBORDOS:
        metro.add_edge(origen, destino, weight=PENALIZACION)

def contar_transbordos(ruta):
    """
    Cuenta la cantidad de transbordos en una ruta usando la lista TRANSBORDOS
    """
    if not ruta or len(ruta) < 2:
        return 0
    
    transbordos = 0
    
    for i in range(len(ruta) - 1):
        estacion_actual = ruta[i]
        estacion_siguiente = ruta[i + 1]
        
        # Verificar si este par es un transbordo definido
        for origen, destino in TRANSBORDOS:
            if (estacion_actual == origen and estacion_siguiente == destino) or \
               (estacion_actual == destino and estacion_siguiente == origen):
                transbordos += 1
                break  # Salir del bucle interno una vez encontrado
    
    return transbordos

# ============================================================================
# 1. CONFIGURACION DEL GRAFO
# ============================================================================

def crear_grafo_metro():
    metro = nx.Graph()
    
    añadir_nodos(metro)
    añadir_aristas(metro)
    añadir_servicios(metro)
    
    return metro

def añadir_nodos(metro):
    # Coordenadas aproximadas
    X_L7 = 190
    X_L3 = 600
    Y_L9 = 290
    Y_L12 = 550
        
    # LINEA 7 
    metro.add_node("Polanco_L7",              pos=(X_L7, 22),  linea="L7", nombre="Polanco")
    metro.add_node("Auditorio_L7",            pos=(X_L7, 115), linea="L7", nombre="Auditorio")
    metro.add_node("Constituyentes_L7",       pos=(X_L7, 200), linea="L7", nombre="Constituyentes")
    metro.add_node("Tacubaya_L7",             pos=(X_L7, Y_L9), linea="L7", nombre="Tacubaya")
    metro.add_node("San Pedro de los Pinos_L7", pos=(X_L7, 400), linea="L7", nombre="San Pedro de los Pinos")
    metro.add_node("San Antonio_L7",          pos=(X_L7, 470), linea="L7", nombre="San Antonio")
    metro.add_node("Mixcoac_L7",              pos=(X_L7, Y_L12), linea="L7", nombre="Mixcoac")
    metro.add_node("Barranca del Muerto_L7",  pos=(X_L7, 630), linea="L7", nombre="Barranca del Muerto")

    # LINEA 3
    metro.add_node("Juarez_L3",              pos=(X_L3, 50),  linea="L3", nombre="Juarez")
    metro.add_node("Balderas_L3",            pos=(X_L3, 110), linea="L3", nombre="Balderas")
    metro.add_node("Ninos Heroes_L3",        pos=(X_L3, 180), linea="L3", nombre="Niños Heroes")
    metro.add_node("Hospital General_L3",    pos=(X_L3, 250), linea="L3", nombre="Hospital General")
    metro.add_node("Centro Medico_L3",       pos=(X_L3, Y_L9), linea="L3", nombre="Centro Medico")
    metro.add_node("Etiopia_L3",             pos=(X_L3, 380), linea="L3", nombre="Etiopia")
    metro.add_node("Eugenia_L3",             pos=(X_L3, 440), linea="L3", nombre="Eugenia")
    metro.add_node("Division del Norte_L3",  pos=(X_L3, 500), linea="L3", nombre="Division del Norte")
    metro.add_node("Zapata_L3",              pos=(X_L3, Y_L12), linea="L3", nombre="Zapata")
    metro.add_node("Coyoacan_L3",            pos=(X_L3, 600), linea="L3", nombre="Coyoacan")
    metro.add_node("Viveros_L3",             pos=(X_L3, 650), linea="L3", nombre="Viveros")
    metro.add_node("M.A. de Quevedo_L3",     pos=(X_L3, 700), linea="L3", nombre="M.A. de Quevedo")
    metro.add_node("Copilco_L3",             pos=(X_L3, 740), linea="L3", nombre="Copilco")
    metro.add_node("Universidad_L3",         pos=(X_L3, 780), linea="L3", nombre="Universidad")

    # LINEA 9
    metro.add_node("Tacubaya_L9",        pos=(X_L7, Y_L9), linea="L9", nombre="Tacubaya")
    metro.add_node("Patriotismo_L9",     pos=(320, Y_L9), linea="L9", nombre="Patriotismo")
    metro.add_node("Chilpancingo_L9",    pos=(460, Y_L9), linea="L9", nombre="Chilpancingo")
    metro.add_node("Centro Medico_L9",   pos=(X_L3, Y_L9), linea="L9", nombre="Centro Medico")
    metro.add_node("Lazaro Cardenas_L9", pos=(700, Y_L9), linea="L9", nombre="Lazaro Cardenas")

    # LINEA 12
    metro.add_node("Mixcoac_L12",            pos=(X_L7, Y_L12), linea="L12", nombre="Mixcoac")
    metro.add_node("Insurgentes Sur_L12",    pos=(320, Y_L12), linea="L12", nombre="Insurgentes Sur")
    metro.add_node("Hospital 20 de Nov_L12", pos=(460, Y_L12), linea="L12", nombre="Hospital 20 de Nov")
    metro.add_node("Zapata_L12",             pos=(X_L3, Y_L12), linea="L12", nombre="Zapata")
    metro.add_node("Parque de los Venados_L12", pos=(700, Y_L12), linea="L12", nombre="Parque de los Venados")
    metro.add_node("Eje Central_L12",        pos=(740, 620), linea="L12", nombre="Eje Central")

    # LINEA 1
    metro.add_node("Observatorio_L1", pos=(604, 1600), linea="L1", nombre="Observatorio")
    metro.add_node("Tacubaya_L1",     pos=(X_L7, Y_L9), linea="L1", nombre="Tacubaya")
    metro.add_node("Juanacatlan_L1",  pos=(250, 270), linea="L1", nombre="Juanacatlan")
    metro.add_node("Chapultepec_L1",  pos=(320, 220), linea="L1", nombre="Chapultepec")
    metro.add_node("Sevilla_L1",      pos=(390, 170), linea="L1", nombre="Sevilla")
    metro.add_node("Insurgentes_L1",  pos=(460, 110), linea="L1", nombre="Insurgentes")
    metro.add_node("Cuauhtemoc_L1",   pos=(530, 110), linea="L1", nombre="Cuauhtemoc")
    metro.add_node("Balderas_L1",     pos=(X_L3, 110), linea="L1", nombre="Balderas")

def añadir_aristas(metro):
    add_tramo(metro, "Polanco_L7", "Auditorio_L7")
    add_tramo(metro, "Auditorio_L7", "Constituyentes_L7")
    add_tramo(metro, "Constituyentes_L7", "Tacubaya_L7")
    add_tramo(metro, "Tacubaya_L7", "San Pedro de los Pinos_L7")
    add_tramo(metro, "San Pedro de los Pinos_L7", "San Antonio_L7")
    add_tramo(metro, "San Antonio_L7", "Mixcoac_L7")
    add_tramo(metro, "Mixcoac_L7", "Barranca del Muerto_L7")

    # L3
    add_tramo(metro, "Juarez_L3", "Balderas_L3")
    add_tramo(metro, "Balderas_L3", "Ninos Heroes_L3")
    add_tramo(metro, "Ninos Heroes_L3", "Hospital General_L3")
    add_tramo(metro, "Hospital General_L3", "Centro Medico_L3")
    add_tramo(metro, "Centro Medico_L3", "Etiopia_L3")
    add_tramo(metro, "Etiopia_L3", "Eugenia_L3")
    add_tramo(metro, "Eugenia_L3", "Division del Norte_L3")
    add_tramo(metro, "Division del Norte_L3", "Zapata_L3")
    add_tramo(metro, "Zapata_L3", "Coyoacan_L3")
    add_tramo(metro, "Coyoacan_L3", "Viveros_L3")
    add_tramo(metro, "Viveros_L3", "M.A. de Quevedo_L3")
    add_tramo(metro, "M.A. de Quevedo_L3", "Copilco_L3")
    add_tramo(metro, "Copilco_L3", "Universidad_L3")

    # L9
    add_tramo(metro, "Tacubaya_L9", "Patriotismo_L9")
    add_tramo(metro, "Patriotismo_L9", "Chilpancingo_L9")
    add_tramo(metro, "Chilpancingo_L9", "Centro Medico_L9")
    add_tramo(metro, "Centro Medico_L9", "Lazaro Cardenas_L9")

    # L12
    add_tramo(metro, "Mixcoac_L12", "Insurgentes Sur_L12")
    add_tramo(metro, "Insurgentes Sur_L12", "Hospital 20 de Nov_L12")
    add_tramo(metro, "Hospital 20 de Nov_L12", "Zapata_L12")
    add_tramo(metro, "Zapata_L12", "Parque de los Venados_L12")
    add_tramo(metro, "Parque de los Venados_L12", "Eje Central_L12")

    # L1
    add_tramo(metro, "Observatorio_L1", "Tacubaya_L1")
    add_tramo(metro, "Tacubaya_L1", "Juanacatlan_L1")
    add_tramo(metro, "Juanacatlan_L1", "Chapultepec_L1")
    add_tramo(metro, "Chapultepec_L1", "Sevilla_L1")
    add_tramo(metro, "Sevilla_L1", "Insurgentes_L1")
    add_tramo(metro, "Insurgentes_L1", "Cuauhtemoc_L1")
    add_tramo(metro, "Cuauhtemoc_L1", "Balderas_L1")
    
    añadir_aristas_transbordo(metro)
    
def añadir_servicios(metro):
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
        
# ============================================================================
# 2. ALGORITMO A* (Heurística y Búsqueda)
# ============================================================================

def heuristica(graph, node_a, node_b):
    """
    Heurística que usa distancias reales (Haversine sobre lat/lon).
    Devuelve tiempo estimado en segundos (distancia_m / VELOCIDAD_METRO).
    """
    lat1, lon1 = HEURISTICA[node_a]
    lat2, lon2 = HEURISTICA[node_b]
    dist_metros = haversine(lat1, lon1, lat2, lon2)

    return dist_metros / VELOCIDAD_METRO

def haversine(lat1, lon1, lat2, lon2):
    """Devuelve la distancia entre dos (lat,lon) en metros usando la fórmula de Haversine."""
    R = 6371000.0  # radio medio de la Tierra en metros
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

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
# 3. INTERFAZ GRAFICA
# ============================================================================

class AppMetro:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro CDMX")
        self.root.geometry("1000x850")
        self.root.resizable(False, False)
        
        self.metro_graph = crear_grafo_metro()
        self.nombres_estaciones = sorted(list(set(
            [data['nombre'] for n, data in self.metro_graph.nodes(data=True)]
        )))
        
        self.node_items = {}
        self.last_route_nodes = []

        # Panel Izquierdo (Controles)
        self.frame_izq = tk.Frame(root, width=500, bg="#f5f5f5", padx=15, pady=15)
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
            nombre_imagen = "Mapa_metro.png"
            imagen_pil = Image.open(nombre_imagen)
            
            scale_factor = 0.24          # Escala
            w, h = imagen_pil.size      # Tamaño original
            new_size = (int(w * scale_factor), int(h * scale_factor))
            imagen_pil = imagen_pil.resize(new_size, Image.LANCZOS)    # Redimensionar

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
            text=f"Estación seleccionada: \n\t{nombre_estacion}\n"
                 f"Escaleras: \n\t{esc}  \nAscensor: {asc}"
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
            transbordos = contar_transbordos(ruta)
            self.lbl_resultado.config(
                text=f"Tiempo aprox: {tiempo_min} min\nEstaciones: {len(ruta)-1-transbordos}\nTransbordos: {transbordos}"
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