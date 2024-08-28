import random
import io 
import base64
import matplotlib.pyplot as plt

def leer_archivo_y_almacenamiento_de_datos(nombre_archivo):
    """lee el archivo y almacena los datos en una matriz(normalizado los str a minusculas)"""
    matriz_peliculas=[]
    with open(nombre_archivo,"r",encoding="UTF-8") as archi:
        linea=archi.readline().strip("\n")
        while linea!="":
            lista_linea=linea.split(";")
            frase_pelicula,pelicula=lista_linea[0].lower(),lista_linea[1].lower()
            fila=[frase_pelicula,pelicula]
            matriz_peliculas.append(fila)
            linea=archi.readline().strip("\n")
    return matriz_peliculas

  

def guardar_resultados(resultados):
    """guarda la informacion por cada jugador de la lista resultados y los guarda en un archivo txt para almacenar
    la informacion"""
    
    archivo_resultados='resultados.txt'
    existen=leer_archivo_existente(archivo_resultados)
    with open(archivo_resultados, 'a') as archivo:
        for resultado in resultados:
            resultado_str = str(resultado)
            usuario = resultado["nombre"]
            puntaje = resultado["puntaje"]
            hora_jugada = resultado["hora"]
            dia = resultado["dia"]
            if resultado_str not in existen:
                existen.add(resultado_str)
                archivo.write( resultado_str + "\n")

def abrir_resultados(archivo_resultados):
    resultados_dias = []
    with open(archivo_resultados, 'r') as archivo:
        for linea in archivo:
            datos = linea.strip().split(',')
            usuario_res = datos[0].split(":")
            usuario = usuario_res[1].strip().strip("'")
            puntaje_res = datos[1].split(":")
            puntaje = puntaje_res[1].strip().strip("'")
            hora_jugada_res = datos[2].split(":")
            horas = hora_jugada_res[1].strip().strip("'")
            minutos = hora_jugada_res[2]
            segundos = hora_jugada_res[3].strip("'")
            hora_jugada = f"{horas}:{minutos}:{segundos}"
            dia_res = datos[3].split(":")
            dia = dia_res[1].strip("}").strip().strip("'")
            resultados_dias.append((usuario, puntaje, hora_jugada, dia))

    return resultados_dias


def leer_archivo_existente(archivo):
    resultados_existentes = set()
    try:
        with open(archivo, 'r') as file:
            for line in file:
                resultados_existentes.add(line.strip())
    except FileNotFoundError:
        # Si el archivo no existe, no hay resultados existentes
        pass
    return resultados_existentes

def leo_y_verifico(archivo):
    with open(archivo, 'r') as arch:
            content = arch.read().strip()
            return content