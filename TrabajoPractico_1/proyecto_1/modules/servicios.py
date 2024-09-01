from modules.dominio import lista_peliculas,obtener_frase_y_opciones,mostrar_grafica_torta,mostrar_grafica
from modules.persistencia import leer_archivo_y_almacenamiento_de_datos,guardar_resultados,abrir_resultados,leer_archivo_existente,leo_y_verifico

def listar_peliculas(archivo):
    matriz = leer_archivo_y_almacenamiento_de_datos(archivo)
    lista = lista_peliculas(matriz)
    return lista

def frase_opciones(archivo,frases_previas):
    matriz=leer_archivo_y_almacenamiento_de_datos(archivo)
    lista_de_peliculas = lista_peliculas(matriz)
    frase_y_opciones=obtener_frase_y_opciones(matriz,lista_de_peliculas,frases_previas)
    frases_previas.append(frase_y_opciones[0])
    return frase_y_opciones

def guardo_paso_resultado(resultados,archivo):
    guardar_resultados(resultados,archivo)
    lista_archivo_resultado=abrir_resultados(archivo)
    return lista_archivo_resultado

def muestro_grafica(resultados,archivo):
    guardar_resultados(resultados,archivo)
    lista_archivo_resultado=abrir_resultados(archivo)
    url=mostrar_grafica(lista_archivo_resultado)
    return url

def muestro_grafica_torta(resultados,archivo):
    guardar_resultados(resultados,archivo)
    lista_archivo_resultado=abrir_resultados(archivo)
    url=mostrar_grafica_torta(lista_archivo_resultado)
    return url

def verifico(archivo):
    x=leo_y_verifico(archivo)
    return x
