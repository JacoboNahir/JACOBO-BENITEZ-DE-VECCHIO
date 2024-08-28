from modules.dominio import lista_peliculas,obtener_frase_y_opciones,mostrar_grafica_torta,mostrar_grafica
from modules.persistencia import leer_archivo_y_almacenamiento_de_datos,guardar_resultados,abrir_resultados,leer_archivo_existente,leo_y_verifico

def listar_peliculas(archivo):
    matriz=leer_archivo_y_almacenamiento_de_datos(archivo)
    lista_de_peliculas=lista_peliculas(matriz)
    return lista_de_peliculas

def frase_opciones(archivo):
    matriz=leer_archivo_y_almacenamiento_de_datos(archivo)
    lista_de_peliculas=lista_peliculas(matriz)
    frase_y_opciones=obtener_frase_y_opciones(matriz,lista_de_peliculas)
    return frase_y_opciones

def guardo_paso_resultado(archivo):
    guardar_resultados(archivo)
    lista_archivo_resultado=abrir_resultados(archivo)
    return lista_archivo_resultado

def muestro_grafica(archivo):
    guardar_resultados(archivo)
    lista_archivo_resultado=abrir_resultados(archivo)
    url=mostrar_grafica(lista_archivo_resultado)

def muestro_grafica_torta(archivo):
    guardar_resultados(archivo)
    lista_archivo_resultado=abrir_resultados(archivo)
    url=mostrar_grafica_torta(lista_archivo_resultado)

def verifico(archivo):
    x=leo_y_verifico(archivo)
    return x
