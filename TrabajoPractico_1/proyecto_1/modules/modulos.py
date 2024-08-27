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

def lista_peliculas(matriz):
    """"crea una lista de las peliculas sin repeticion y las ordena alfabeticamente"""
    lista_peliculas=[]
    for i in matriz:
        if i[1] not in lista_peliculas:
            lista_peliculas.append(i[1])
    return sorted(lista_peliculas)  
              
def obtener_frase_y_opciones(matriz_peliculas,lista_peliculas):
    """encuentra una frase al azar, su opcion corecta y dos opciones incorrectas"""
    frases = set(frase for frase, _ in matriz_peliculas)
    """Crear un conjunto de frases:Se utiliza una comprensión de conjunto para extraer todas las frases de matriz_peliculas. Aquí, frase es la 
    primera parte de cada tupla y _ se usa para ignorar la segunda parte (la película). Al usar un conjunto (set), se eliminan las frases 
    duplicadas.
    """
    frase_aleatoria = random.choice(list(frases))
    """Seleccionar una frase aleatoria: Se convierte el conjunto de frases a una lista y se utiliza random.choice() para seleccionar una frase 
    aleatoria de esa lista.
    """
    pelicula_correcta = next(pelicula for frase, pelicula in matriz_peliculas if frase == frase_aleatoria)  
    """Encontrar la película correcta**: Se busca la película que corresponde a la frase_aleatoria. next() se usa para obtener la primera 
    película que coincide con la frase seleccionada. Esto supone que hay una relación uno a uno entre las frases y las películas.
    """
    opciones = [pelicula for pelicula in lista_peliculas if pelicula != pelicula_correcta]
    """Crear una lista de opciones incorrectas: Se utiliza otra comprensión de lista para crear una nueva lista llamada opciones que contiene todas 
    las películas de lista_peliculas, excluyendo la pelicula_correcta.
    """
    if len(opciones) < 2:
        raise ValueError("No hay suficientes opciones disponibles")
    """Verificación de opciones: Se comprueba si hay al menos dos opciones incorrectas disponibles. Si no es así, se lanza un error (ValueError) 
    indicando que no hay suficientes opciones.
    """    
    opciones_aleatorias = random.sample(opciones, 2)
    """Seleccionar opciones incorrectas aleatorias**: Se usa random.sample() para seleccionar dos opciones incorrectas aleatorias de la lista 
    opciones.
    """
    opciones_aleatorias.append(pelicula_correcta)
    """Agregar la opción correcta: Se añade la pelicula_correcta a la lista opciones_aleatorias, que ahora tiene una opción correcta y dos 
    incorrectas.
    """
    random.shuffle(opciones_aleatorias)
    """Mezclar las opciones: Se reorganizan aleatoriamente las opciones en opciones_aleatorias para que la posición de la película correcta sea 
    aleatoria entre las opciones.
    """
    return frase_aleatoria, opciones_aleatorias, pelicula_correcta

def keep_resultados(resultados):
    """guarda la informacion por cada jugador de la lista resultados y los guarda en un archivo txt para almacenar
    la informacion"""
    resultados_dias = []
    with open('resultados.txt', 'a') as archivo:
        for resultado in resultados:
            usuario = resultado["nombre"]
            puntaje = resultado["puntaje"]
            hora_jugada = resultado["hora"]
            dia = resultado["dia"]
            archivo.write(f"{usuario},{puntaje},{hora_jugada},{dia}\n")

    with open('resultados.txt', 'r') as archivo:
        for linea in archivo:
            datos = linea.strip().split(',')
            usuario = datos[0]
            puntaje = datos[1]  
            hora_jugada = datos[2]
            dia = datos[3]
            resultados_dias.append((usuario, puntaje, hora_jugada, dia))

    return resultados_dias

def mostrar_grafica_torta(resultados_dias):
    """obtiene los aciertos y desaciertos totales de cada jugador y hace la grafica de la torta"""
    if resultados_dias:
        resultados_dias.pop(0)
    aciertos = []
    desaciertos = []
    for linea in resultados_dias:
        puntaje = str(linea[1])
        aciertos_str, desaciertos_str = puntaje.split('/')
        cantidad_aciertos = int(aciertos_str)
        cantidad_desaciertos = int(desaciertos_str)
        aciertos.append(cantidad_aciertos)
        desaciertos.append(cantidad_desaciertos - cantidad_aciertos)  

    total_aciertos = sum(aciertos)
    total_desaciertos = sum(desaciertos)

    plt.figure(figsize=(6, 6))
    plt.pie([total_aciertos, total_desaciertos], labels=['Aciertos', 'Desaciertos'], autopct='%1.1f%%', colors=['green', 'red'])
    plt.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64_1 = base64.b64encode(img.getvalue()).decode()
    img_url = f'data:image/png;base64,{img_base64_1}'

    return img_url

def mostrar_grafica(resultados_dias):
    """obtiene los aciertos y desaciertos totales de cada jugador y hace la grafica de curvas"""
    if resultados_dias:
        resultados_dias.pop(0)
    resultados_agrupados = {}

    for linea in resultados_dias:
        nombre=linea[0]
        puntaje=str(linea[1])
        dia=linea[-1]
        print(puntaje)
        aciertos_str, total = puntaje.split('/')
        aciertos = int(aciertos_str)
        desaciertos = int(total) - aciertos
        clave = (nombre, dia)

        if clave in resultados_agrupados:
            resultados_agrupados[clave]['aciertos'] += aciertos
            resultados_agrupados[clave]['desaciertos'] += desaciertos
        else:
            resultados_agrupados[clave] = {'aciertos': aciertos, 'desaciertos': desaciertos}

    nombres_dias = []
    aciertos_totales = []
    desaciertos_totales = []

    for clave, resultados in resultados_agrupados.items():
        nombre, dia = clave
        aciertos_totales.append(resultados['aciertos'])
        desaciertos_totales.append(resultados['desaciertos'])
        nombres_dias.append(f'{nombre} - {dia}')

    fig, ax = plt.subplots()
    ax.plot(nombres_dias, desaciertos_totales, label='Desaciertos', color="#AF7AC5", marker='o')
    ax.plot(nombres_dias, aciertos_totales, label='Aciertos', color='#2ECC71', marker='o')

    ax.set_xlabel("Fecha y Usuario", fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'tab:blue'})
    ax.set_ylabel("Cantidad")
    ax.tick_params(axis='x', labelsize=7)

    m_a = max(aciertos_totales)
    m_d = max(desaciertos_totales)
    if m_a < m_d:
        ax.set_ylim([0, m_d + 5]) 
        ax.set_yticks(range(0, m_d + 5, 5))  
    else:
        ax.set_ylim([0, m_a + 5])  
        ax.set_yticks(range(0, m_a + 5, 5)) 

    ax.legend(loc='upper right')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.subplots_adjust(bottom=0.25)

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    img_url_2 = f'data:image/png;base64,{grafico_data}'

    return img_url_2