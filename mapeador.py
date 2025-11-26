import tkinter as tk
from PIL import Image, ImageTk
import json
import os

# LISTA DE ESTACIONES QUE QUEREMOS UBICAR
ESTACIONES = [
    "Polanco", "Auditorio", "Constituyentes", "Tacubaya", 
    "San Pedro de los Pinos", "San Antonio", "Mixcoac", "Barranca del Muerto",
    "Juarez", "Balderas", "Ninos Heroes", "Hospital General", "Centro Medico",
    "Etiopia", "Eugenia", "Division del Norte", "Zapata", "Coyoacan", 
    "Viveros", "M.A. de Quevedo", "Copilco", "Universidad",
    "Observatorio", "Juanacatlan", "Chapultepec", "Sevilla", "Insurgentes", "Cuauhtemoc",
    "Patriotismo", "Chilpancingo", "Lazaro Cardenas",
    "Insurgentes Sur", "Hospital 20 de Nov", "Parque de los Venados", "Eje Central"
]

class Mapeador:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Mapeo de Estaciones")
        
        self.mapa_path = "Mapa_metro_sin_margen.png"
        if not os.path.exists(self.mapa_path):
            print(f"Error: No encuentro {self.mapa_path}. Ejecuta el script principal primero para recortar la imagen.")
            root.destroy()
            return

        # Cargar imagen (sin redimensionar para obtener coords reales)
        self.img_pil = Image.open(self.mapa_path)
        self.tk_img = ImageTk.PhotoImage(self.img_pil)
        
        self.canvas = tk.Canvas(root, width=self.img_pil.width, height=self.img_pil.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        
        self.canvas.bind("<Button-1>", self.guardar_punto)
        
        self.index = 0
        self.datos = {}
        
        self.lbl_instruccion = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="yellow")
        self.lbl_instruccion.pack(fill="x")
        
        self.actualizar_etiqueta()

    def actualizar_etiqueta(self):
        if self.index < len(ESTACIONES):
            nombre = ESTACIONES[self.index]
            self.lbl_instruccion.config(text=f"Haz CLICK en: {nombre.upper()} ({self.index + 1}/{len(ESTACIONES)})")
        else:
            self.lbl_instruccion.config(text="¡TERMINADO! Archivo 'coordenadas_metro.json' guardado.", bg="#00ff00")
            self.guardar_json()

    def guardar_punto(self, event):
        if self.index >= len(ESTACIONES): return
        
        nombre = ESTACIONES[self.index]
        x, y = event.x, event.y
        
        # Guardar en diccionario
        self.datos[nombre] = (x, y)
        
        # Dibujar puntito visual
        r = 5
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="red", outline="white")
        
        print(f"Guardado {nombre}: {x}, {y}")
        self.index += 1
        self.actualizar_etiqueta()

    def guardar_json(self):
        with open("coordenadas_metro.json", "w") as f:
            json.dump(self.datos, f, indent=4)
        print("Archivo JSON generado correctamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Mapeador(root)
    root.mainloop()