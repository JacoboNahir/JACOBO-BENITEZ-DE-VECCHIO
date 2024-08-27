from flask import render_template, request, redirect, url_for, session
from modules.config import app
from modules.modulos import leer_archivo_y_almacenamiento_de_datos,lista_peliculas,obtener_frase_y_opciones,keep_resultados,mostrar_grafica_torta,mostrar_grafica
import random
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

app.secret_key = 'llave_para_seguridad'

matriz_peliculas=leer_archivo_y_almacenamiento_de_datos("frases_de_peliculas.txt")

""" Decorador @app.route("/"): Este decorador define una ruta en la aplicación web. En este caso, la ruta es la raíz ("/"), lo que significa que esta 
función se ejecutará cuando un usuario acceda a la URL principal de la aplicación.
Métodos ["GET", "POST"]: Se especifica que la función inicio puede manejar tanto solicitudes GET como POST.
GET: Normalmente se utiliza para obtener datos.
POST: Se utiliza para enviar datos al servidor. """
@app.route("/", methods=["GET", "POST"]) 

def inicio():#función que se ejecuta cuando se accede a la ruta definida.
    if request.method == "POST":
        session["num_intentos"] = int(request.form["num_intentos"])
        """Almacena el número de intentos (enviado desde un formulario) en la sesión del usuario. session se utiliza para mantener datos entre 
        diferentes solicitudes del mismo usuario."""
        session["usuario"] = request.form["usuario"] ; """Almacena el nombre de usuario proporcionado en el formulario."""        
        session["frases_previas"] = [] ; """Inicializa una lista vacía para almacenar frases anteriores."""        
        session["aciertos"] = 0 ; """Inicializa el contador de aciertos a cero.""" 
        peliculas =lista_peliculas(matriz_peliculas)
        frase, opciones_mezcladas, pelicula_correcta = obtener_frase_y_opciones(matriz_peliculas,peliculas)
        session["frase"] = frase ; """Almacena la frase generada en la sesión."""
        session["opciones_mezcladas"] = opciones_mezcladas ; """Almacena las opciones mezcladas."""
        session["pelicula_correcta"] = pelicula_correcta ; """Almacena la película correcta."""
        session["cont"] = 0 ; """Inicializa un contador a cero."""

        if session["num_intentos"]>=3:
            return redirect(url_for("introduccion")) 
        mensaje = "El número mínimo son 3."
        """Comprueba si el número de intentos es mayor o igual a 3.
          - Si es así, redirige al usuario a la ruta introduccion mediante return redirect(url_for("introduccion")).
          - Si no, devuelve un mensaje que indica que el número mínimo de intentos es 3 y renderiza la plantilla jugar.html con ese mensaje."""
        return render_template("jugar.html", mensaje=mensaje)

    return render_template("inicio.html")
"""Si la solicitud es de tipo GET, simplemente se renderiza la plantilla inicio.html, que probablemente 
muestre un formulario o una pantalla de bienvenida."""

@app.route("/introduccion", methods=["GET", "POST"])#define una nueva ruta en la aplicación web que responderá a las solicitudes a la URL /introduccion. 
def introduccion():#se ejecutará cuando un usuario acceda a la ruta /introduccion.
    if request.method == "POST":
        return redirect(url_for("jugar"))#se utiliza redirect(url_for("jugar")) para redirigir al usuario a otra ruta llamada jugar.
    #url_for("jugar") genera la URL correspondiente a la función jugar, lo que permite que se redirija al usuario a la página o función correspondiente de forma segura y dinámica.
    return render_template("introduccion.html")
"""Si la solicitud no es un POST (es decir, es un GET), se renderiza una plantilla HTML llamada introduccion.html. 
Esto significa que el usuario verá esta página cuando acceda a la URL /introduccion sin haber enviado un formulario."""
                           
resultados=[]
@app.route("/jugar", methods=["GET", "POST"])
def jugar():#se ejecutará cuando un usuario acceda a la ruta /jugar.
    if request.method == "POST":
        num_intentos = session["num_intentos"]#Se recupera el número de intentos permitidos desde la sesión del usuario y se almacena en la variable
        if session["cont"] >= session["num_intentos"]:#se verifica si el contador de intentos (session["cont"]) ha alcanzado o superado el número 
        #máximo de intentos (session["num_intentos"]).
            """Almacenamiento de resultados en la sesión"""
            session["nombre"] = session.get("usuario")#Se guarda el nombre del usuario en la sesión.
            session["hora_jugado"] = datetime.now().strftime("%H:%M:%S")#Se obtiene la hora 
            session["dia"] = datetime.now().strftime("%d/%m/%Y")#se obtiene el dia
            session["aciertos"] = session.get("aciertos", 0)#Se recuperan los aciertos del usuario (o se establece en 0 si no hay datos) y se calcula 
            session["puntaje"] = f"{session['aciertos']}/{session['num_intentos']}"# el puntaje en formato aciertos/número de intentos.
            resultados.append({"nombre": session["nombre"], "puntaje": session["puntaje"], "hora": session["hora_jugado"], "dia": session["dia"]})
            """Se agrega un diccionario con los detalles del usuario (nombre, puntaje, hora de juego y día) a la lista resultados."""
            return redirect("/resultado_local") #Después de que el usuario ha terminado el juego, se redirige a una ruta llamada 
        #resultado_personal, donde se mostrarán los resultados del juego.
 
        return render_template("jugar.html", num_intentos=session["num_intentos"],
                               frases_seleccionada=session["frase"], opciones=session['opciones_mezcladas'],
                               pelicula_correcta=session['pelicula_correcta'])
    """Si el usuario aún no ha alcanzado el límite de intentos, se renderiza la plantilla jugar.html con varios datos pasados como contexto:
      - num_intentos: el número máximo de intentos.
      - frases_seleccionada: la frase que se está usando en el juego.
      - opciones: las opciones de respuesta mezcladas.
      - pelicula_correcta: la película que es la respuesta correcta."""

    return render_template("jugar.html", num_intentos=session["num_intentos"],
                           frases_seleccionada=session['frase'], opciones=session['opciones_mezcladas'],
                           pelicula_correcta=session['pelicula_correcta'])
"""Si la solicitud no es de tipo POST (es GET), simplemente se renderiza de nuevo la plantilla jugar.html con la misma información."""


@app.route("/mensaje", methods=["POST"])

def mensaje():
    if request.method == 'POST':
        opcion_seleccionada = request.form.get("opcion_seleccionada")#obtiene la opción que el usuario ha seleccionado del formulario. 
        #request.form.get() busca el valor asociado a la clave "opcion_seleccionada".
        pelicula_correcta=session["pelicula_correcta"]#Se recupera la respuesta correcta almacenada en la sesión, que se había establecido en pasos anteriores del juego.
        print(f'la respuesta correcta es {len(pelicula_correcta)}')
        print(f'la opcion seleccionada es {len(opcion_seleccionada)}')
        print(pelicula_correcta == opcion_seleccionada)#Se imprime el resultado de la comparación entre la respuesta correcta y la opción seleccionada. Esto mostrará True o False.
        if pelicula_correcta.strip() == opcion_seleccionada.strip() :
            mensaje = "¡Correcto!"
            session['aciertos'] += 1  
        else:
            mensaje = f"¡Incorrecto! La respuesta correcta era: {pelicula_correcta}"

        session['cont'] += 1#Se incrementa el contador de intentos en la sesión
        print(mensaje)
        print(session['frase'])

        #genera una nueva frase y opciones para el proximo juego
        peliculas = lista_peliculas(matriz_peliculas)
        frase, opciones_mezcladas, pelicula_correcta = obtener_frase_y_opciones(matriz_peliculas,peliculas)
        session["frase"] = frase
        session["opciones_mezcladas"] = opciones_mezcladas
        session["pelicula_correcta"] = pelicula_correcta
        """Las variables para la nueva frase, opciones y respuesta correcta se almacenan en la sesión para poder usarlas en la siguiente interacción."""
        
        return render_template("mensaje.html", mensaje=mensaje, opcion_seleccionada=opcion_seleccionada, pelicula_correcta=pelicula_correcta)
    """Finalmente, se renderiza una plantilla HTML llamada mensaje.html, pasándole la información del mensaje, la opción seleccionada por el usuario
    y la película correcta. Esto permite mostrar al usuario los resultados de su respuesta en la interfaz."""

@app.route("/listar_peliculas")#No se especifican métodos en esta línea, lo que significa que esta ruta manejará solicitudes GET por defecto.
#define una ruta en la aplicación web que responde a las solicitudes dirigidas a la URL /listar_peliculas
def listar_peliculas():#se ejecutará cuando un usuario acceda a la ruta /listar_peliculas.
    peliculas = lista_peliculas(matriz_peliculas)
    x = len(peliculas)
    return render_template("listar.html", peliculas=peliculas, x=x)
"""se utiliza la función render_template para generar la respuesta HTML utilizando la plantilla listar.html.
- Se pasa la variable peliculas a la plantilla, que contendrá la lista de películas obtenida anteriormente. Esto permite que la plantilla acceda a 
esa información para mostrarla en la interfaz de usuario."""


@app.route("/resultado_local")
def resultado_personal():
    nombre = session.get("nombre","None")# Se obtiene el valor asociado a la clave "nombre" de la sesión. Si no existe, nombre será None.
    hora_jugado = session.get("hora_jugado")#Se obtiene el valor de la clave "hora_jugado" de la sesión, que indica a qué hora se jugó la partida.
    puntaje = session.get("puntaje", "0/0")#se obtiene el puntaje del usuario de la sesión. Si no se encuentra el puntaje, se asigna un valor por defecto de "0/0".
    dia=session["dia"]#Se obtiene el valor de la clave "dia" de la sesión, que normalmente representa el día en que se jugó.
    return render_template("resultado_local.html", nombre=nombre, hora_jugado=hora_jugado, puntaje=puntaje, dia=dia)
"""renderiza la plantilla resultado_local.html y le pasa como contexto las variables nombre, hora_jugado, puntaje y dia. Esto permite que
la plantilla use estos valores para mostrar información personalizada al usuario, como su nombre, la hora de juego, el puntaje obtenido y el día de 
la partida."""

@app.route("/resultados_globales")
def resultados_globales():
    guardar=keep_resultados(resultados)
    """se llama a la función guardar_resultados, pasándole la lista resultados como argumento. guarda la 
    informacion por cada jugador de la lista resultados y los guarda en un archivo txt para almacenar la informacion"""
    return render_template("resultado_global.html", resultados=resultados)
"""Finalmente, la función devuelve una respuesta que renderiza la plantilla resultado_global.html.
- Se le pasa la lista resultados como un contexto a la plantilla, lo que permitirá que los resultados se muestren en la interfaz de usuario."""

def ver_grafico():
    resultados = session.get('resultados', [])
    """se obtiene una lista de resultados de la sesión utilizando session.get(). Si no hay resultados guardados, se asigna una lista vacía como 
    valor predeterminado."""
    nombre_archivo = 'grafico_torta.png'
    """Se define el nombre del archivo que se va a guardar (grafico_torta.png)."""
    ruta_archivo = f'static/{nombre_archivo}'
    """se crea una ruta para el archivo combinando la carpeta static con el nombre del archivo. Esto es importante en aplicaciones web, ya que la 
    carpeta static es donde se suelen guardar archivos como imágenes, CSS y JavaScript que se sirven al cliente."""
    plt.savefig(ruta_archivo)
    """utiliza la biblioteca Matplotlib para guardar el gráfico en la ruta especificada. """
    
    return render_template("ver_graficos.html", ruta_archivo=nombre_archivo)
"""Finalmente, la función devuelve el resultado de render_template, que renderiza la plantilla ver_graficos.html.
- Se pasa el nombre_archivo como argumento a la plantilla, lo que permite que la plantilla acceda a la ubicación del gráfico para mostrarlo al usuario."""
#En resumen, esta función obtiene resultados de la sesión, genera un gráfico y lo guarda en una ubicación específica, y luego muestra ese gráfico en 
#una plantilla web.

@app.route("/mostrar_grafica")
def mostrar_grafica_curvas():
    resultados_dias = keep_resultados(resultados)
    img_url_2 = mostrar_grafica(resultados_dias)#mostrar_grafica`genera una gráfica y devuelve la URL o la ruta del archivo de imagen de la gráfica generada, que se guarda en `img_url_2.
    return render_template("mostrar_grafica.html", img_url_2=img_url_2)
"""Finalmente, la función retorna el resultado de render_template, que renderiza la plantilla mostrar_grafica.html.
- Se pasa img_url_2 como argumento a la plantilla, lo que permite que la página web acceda a la imagen generada y la muestre."""

#En resumen, la función mostrar_grafica_curvas se encarga de procesar los resultados, generar una gráfica a partir de ellos y renderizar una página 
#que muestra esa gráfica.
@app.route("/mostrar_grafica_torta")
def mostrar_grafica_tortita():
        resultado_dias=keep_resultados(resultados)
        img_url = mostrar_grafica_torta(resultado_dias)#devolverá la URL de la imagen generada, que se almacena en img_url.  
        return render_template("mostrar_grafica_torta.html", img_url=img_url)
"""- Finalmente, se utiliza render_template para renderizar la plantilla HTML llamada mostrar_grafica_torta.html.
- Se pasa img_url a la plantilla, lo que permite mostrar la gráfica de torta en la página web."""
#En resumen, esta función maneja la solicitud para mostrar una gráfica de torta, procesando los resultados almacenados, generando la gráfica y 
#renderizando la página correspondiente para mostrarla.
if __name__ == "__main__":#verifica si el script se está ejecutando como el programa principal. En Python, cada archivo tiene un 
#atributo __name__. Si el archivo se ejecuta directamente, __name__ se establece en "__main__". Si el archivo se importa como un módulo en otro 
#script, __name__ tendrá el nombre del archivo.
    app.run(debug=True)
    """- Esta línea inicia el servidor web de la aplicación Flask.
    - El argumento debug=True habilita el modo de depuración. Esto significa que se proporcionará información de depuración útil y que la aplicación 
    se reiniciará automáticamente si haces cambios en el código. También mostrará errores detallados en el navegador si ocurren excepciones."""

#Este bloque de código permite ejecutar la aplicación Flask directamente desde el archivo cuando se ejecuta como el script principal. Al establecer 
#debug=True, facilita el desarrollo al proporcionar actualizaciones automáticas y mensajes de error detallados.