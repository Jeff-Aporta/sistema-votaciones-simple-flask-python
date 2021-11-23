# Ejecutar ▶
# pip install flask

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor corriendo desde Python - Flask"

app.run(debug=True, host="0.0.0.0")
