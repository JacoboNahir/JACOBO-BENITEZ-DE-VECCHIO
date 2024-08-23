from modules.config import app

 
app= Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Nahir lavá el edi</p>"

@app.route ("/bye")
def bye_world():
    return "<p>Bye Bye 👆🧏‍♂️</p>"

if __name__ == "__main__":
    app.run(debug=True)
