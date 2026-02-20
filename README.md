# Metro CDMX - Calculadora de Rutas
Una aplicación de escritorio desarrollada en Python para calcular rutas y tiempos de viaje estimados en el sistema de Metro de la Ciudad de México.

> [!Warning]
> Se trata de un proyecto académico realizado en pocas semanas, por lo que su cobertura se limita a una sección del sistema del Metro de la Ciudad de México y no abarca toda la red. Asimismo, puede presentar limitaciones de rendimiento (especialmente en Windows) o problemas relacionados con el tamaño de la ventana, ya que no contamos con amplia experiencia en Python ni en sus librerías. Para más detalles consulta la sección de [Notas](#Notas).

> [!Note]
> Puede visualizar el archivo ppt del proyecto haciendo click
> [aquí](https://www.canva.com/design/DAG6dDJUXF8/CQd0U0vlWWYd-ESSwZLuug/view?utm_content=DAG6dDJUXF8&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h306a0f4a96)

## Características
- 🗺️ **Visualización interactiva**: Mapa del Metro CDMX con resaltado de la ruta calculada
- ⏱️ **Cálculo de rutas óptimas**: Utiliza el algoritmo A* para encontrar el camino más rápido
- ♿ **Filtros de accesibilidad**: Opciones para usuarios que requieren escaleras electromecánicas o ascensores
- 📊 **Información detallada**: Muestra tiempo estimado, número de estaciones y transbordos

## Tecnologías utilizadas
- Python 3
- Tkinter (interfaz gráfica)
- NetworkX (modelado del grafo)
- Pillow (carga y redimensionado de imagen)
- heapq (cola de prioridad para A*)

## Uso
1. Seleccionar estación de origen.
2. Seleccionar estación de destino.
3. Opcionalmente activar filtros de accesibilidad.
4. Pulsar "BUSCAR RUTA".
5. La aplicación mostrará:
   - Tiempo aproximado.
   - Número de estaciones.
   - Número de transbordos.
   - Ruta resaltada en el mapa.

## Notas
- Las distancias y coordenadas son aproximadas.
- El modelo incluye un subconjunto de líneas.
- El tiempo calculado es una estimación teórica basada en velocidad constante.
- Los servicios de accesibilidad se consideran únicamente en transbordos.
