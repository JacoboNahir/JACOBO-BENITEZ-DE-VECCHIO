import random

def leer_archivo_y_almacenamiento_de_datos(nombre_archivo):
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

def lista_peliculas(matriz):
    lista_peliculas=[]
    for i in matriz:
        if i[1] not in lista_peliculas:
            lista_peliculas.append(i[1])
    return sorted(lista_peliculas)

def obtener_frase_y_opciones(matriz_peliculas, lista_peliculas,cantidad_opciones):
    """encuentra una frase al azar, su opcion corecta y dos opciones incorrectas"""
    frases = set(frase for frase,_ in matriz_peliculas)  
    frase_aleatoria = random.choice(list(frases))  
    pelicula_correcta = next(pelicula for frase, pelicula in matriz_peliculas if frase == frase_aleatoria)  
    
    opciones = [pelicula for pelicula in lista_peliculas if pelicula != pelicula_correcta]
    if len(opciones) < 2:
        raise ValueError("No hay suficientes opciones disponibles")
    
    opciones_aleatorias = random.sample(opciones, cantidad_opciones-1)
    opciones_aleatorias.append(pelicula_correcta)
    random.shuffle(opciones_aleatorias)
    
    return frase_aleatoria, opciones_aleatorias, pelicula_correcta

a=leer_archivo_y_almacenamiento_de_datos("frases_de_peliculas.txt")
b=lista_peliculas(a)
c=obtener_frase_y_opciones(a,b,3)
print(c)
