from flask import render_template
from modules.config import app

@app.route("/")
def inicio():
    return render_template('inicio.html')

@app.route ("/lista")
def lista():
    return render_template('lista.html')

@app.route ("/resultados")
def resultados():
    return render_template('resultados.html')

@app.route ("/graficas")
def graficas():
    return render_template('graficas.html')

@app.route ("/juego")
def juego():
    return render_template('juego.html')

if __name__ == "__main__":
    app.run(debug=True)
