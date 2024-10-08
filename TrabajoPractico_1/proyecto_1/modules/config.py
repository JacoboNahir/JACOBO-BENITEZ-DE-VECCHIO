from flask import Flask
from flask_session import Session

app = Flask("main")
SESSION_TYPE= 'filesystem'
app.config.from_object(__name__)
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"

Session(app)


app.secret_key = 'llave_para_seguridad'