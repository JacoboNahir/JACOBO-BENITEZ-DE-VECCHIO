import random
import io 
import base64
import matplotlib.pyplot as plt

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
    frase_aleatoria = random.choice(list(frases))
    pelicula_correcta = next(pelicula for frase, pelicula in matriz_peliculas if frase == frase_aleatoria)  
    opciones = [pelicula for pelicula in lista_peliculas if pelicula != pelicula_correcta]
    
    if len(opciones) < 2:
        raise ValueError("No hay suficientes opciones disponibles")
     
    opciones_aleatorias = random.sample(opciones, 2)
    opciones_aleatorias.append(pelicula_correcta)
    random.shuffle(opciones_aleatorias)
    
    return frase_aleatoria, opciones_aleatorias, pelicula_correcta

def mostrar_grafica_torta(resultados_dias):
    """obtiene los aciertos y desaciertos totales de cada jugador y hace la grafica de la torta"""

    aciertos = []
    desaciertos = []
    for linea in resultados_dias:
        puntaje = str(linea[1])
        aciertos_str, desaciertos_str = puntaje.split('/')
        cantidad_aciertos = int(aciertos_str)
        cantidad_desaciertos = int(desaciertos_str)
        aciertos.append(cantidad_aciertos)
        desaciertos.append(cantidad_desaciertos - cantidad_aciertos)  

    total_aciertos = 0       
    total_desaciertos = 0

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
    
    resultados_agrupados = {}


    for linea in resultados_dias:
        nombre=linea[0]
        puntaje=str(linea[1])
        dia=linea[-1]

        aciertos_str, total = puntaje.split('/')
        aciertos = int(aciertos_str)
        desaciertos = int(total) - aciertos

        clave = (dia)
        if clave in resultados_agrupados:
            resultados_agrupados[clave]['aciertos']+= aciertos
            resultados_agrupados[clave]['desaciertos']+= desaciertos
        else:
            resultados_agrupados[clave] = {'aciertos': aciertos, 'desaciertos': desaciertos}

    dias_juego = []
    aciertos_totales = []
    desaciertos_totales = []

    for clave, resultados in resultados_agrupados.items():
        dia = clave
        aciertos_totales.append(resultados['aciertos'])
        desaciertos_totales.append(resultados['desaciertos'])
        dias_juego.append(f'{dia}')

    fig, ax = plt.subplots()
    ax.plot(dias_juego, desaciertos_totales, label='Desaciertos', color="#AF7AC5", marker='o')
    ax.plot(dias_juego, aciertos_totales, label='Aciertos', color='#2ECC71', marker='o')

    ax.set_xlabel("Fecha", fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'tab:blue'})
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
