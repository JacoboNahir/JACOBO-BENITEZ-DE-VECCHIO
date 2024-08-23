from flask import Flask, render_template
from modules.config import app
from modules.modulos import leer_archivo_y_almacenamiento_de_datos, lista_peliculas, obtener_frase_y_opciones

@app.route("/")
def inicio():
    return render_template('inicio.html')

@app.route ("/lista")
def lista():
    matriz_de_películas_y_frases = leer_archivo_y_almacenamiento_de_datos("frases_de_peliculas.txt")
    lista_completa = lista_peliculas(matriz_de_películas_y_frases)
    return render_template('lista.html',peliculas=lista_peliculas)

@app.route ("/resultados")
def resultados():
    return render_template('resultados.html')

@app.route ("/graficas")
def graficas():
    return render_template('graficas.html')

@app.route ("/juego")
def juego():
    a=leer_archivo_y_almacenamiento_de_datos("frases_de_peliculas.txt")
    b=lista_peliculas(a)
    c=obtener_frase_y_opciones(a,b,3)
    return render_template('juego.html',a,b,c)

if __name__ == "__main__":
    app.run(debug=True)
