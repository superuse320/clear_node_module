import os # se uso para listar los archivos del directorio
import shutil # se uso para eliminar los directorios
from datetime import datetime 

def calcular_tamaño_carpeta(ruta_carpeta):
    tamaño_total = 0
    for ruta_directorio, _, archivos in os.walk(ruta_carpeta):
        for archivo in archivos:
            tamaño_total += os.path.getsize(os.path.join(ruta_directorio, archivo))
    return tamaño_total

def buscar_y_mostrar_node_modules(directorio_base):
    rutas_node_modules = []
    print("Buscando carpeta ...\n")
    for ruta_directorio, subdirectorios, _ in os.walk(directorio_base):
        if 'node_modules' in subdirectorios:
            ruta_carpeta = os.path.join(ruta_directorio, 'node_modules')
            tamaño_carpeta = calcular_tamaño_carpeta(ruta_carpeta)
            fecha_modificacion = os.path.getmtime(ruta_carpeta)
            fecha_formateada = datetime.fromtimestamp(fecha_modificacion).strftime('%Y-%m-%d %H:%M:%S')
            rutas_node_modules.append((ruta_carpeta, tamaño_carpeta, fecha_formateada))
    
    return rutas_node_modules

def mostrar_carpetas_encontradas(lista_carpetas_node_modules):
    print("Carpetas 'node_modules' encontradas:\n")
    for indice, (ruta, tamaño, fecha) in enumerate(lista_carpetas_node_modules):
        tamaño_en_mb = tamaño / (1024 * 1024)  
        print(f"{indice + 1}. {ruta} - Tamaño: {tamaño_en_mb:.2f} MB - Última modificación: {fecha}")
def eliminar_carpetas(seleccion_indices, lista_carpetas_node_modules):
    espacio_total_liberado = 0
    for indice in seleccion_indices:
        ruta_carpeta, tamaño_carpeta, _ = lista_carpetas_node_modules[indice]
        try:
            shutil.rmtree(ruta_carpeta)
            espacio_total_liberado += tamaño_carpeta
            print(f"Carpeta eliminada: {ruta_carpeta}")
        except Exception as error:
            print(f"Error al eliminar la carpeta {ruta_carpeta}: {error}")
    return espacio_total_liberado


directorio_base = input("Ingresa el directorio : ")
lista_carpetas_node_modules = buscar_y_mostrar_node_modules(directorio_base)
if not lista_carpetas_node_modules:
    print("No se encontraron carpetas 'node_modules'.")
    exit()

mostrar_carpetas_encontradas(lista_carpetas_node_modules)
seleccion_indices = input("Ingresa los números de las carpetas a eliminar, separados por comas: ")
seleccion_indices = [int(i) - 1 for i in seleccion_indices.split(',')]  
espacio_liberado = eliminar_carpetas(seleccion_indices, lista_carpetas_node_modules)
espacio_liberado_en_mb = espacio_liberado / (1024 * 1024)
print(f"Espacio liberado: {espacio_liberado_en_mb:.2f} MB")

