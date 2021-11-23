# Instaladas
from flask import Flask, render_template, request, redirect
# python
import random  # para escoger personas aleatorias de la db de google calc
import urllib.request  # para leer la db de google calc
import json  # para comunicar más fácilmente js con python

# propias
from app_mysql import *

app = Flask(__name__)

crearTabla(
    "votante",
    '''
        _id varchar(15) primary key,
        nombre varchar(255) not null,
        apellido varchar(255) not null,
        tipodoc varchar(10) not null,
        genero varchar(1) not null,
        localidad varchar(255) not null
    '''
)
crearTabla(
    "candidato",
    '''
        _id varchar(15) primary key,
        nombre varchar(255) not null,
        apellido varchar(255) not null,
        tipodoc varchar(10) not null,
        partido varchar(255) not null,
        localidad varchar(255) not null
    '''
)

crearTabla(
    "votacion",
    '''
        _id_votante varchar(15) primary key,
        _id_candidato varchar(15)
    '''
)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/borrar-tablas')
def borrar_tablas():
    borrar_datos_tabla("votante")
    borrar_datos_tabla("candidato")
    borrar_datos_tabla("votacion")
    return redirect("/")


@app.route('/datos-prueba')
def datos_prueba():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQrgTePZuWpbJA7r5Xgi2Ub2S69ND-aP753MghAxImCfEKLM_5RwjEHu3DgRCSYfy7tWL4dGLVLdhX2/pub?output=tsv"
    file = urllib.request.urlopen(url)
    i = 0
    nombres = []
    for line in file:
        decoded_line = line.decode("utf-8")
        nombres.append(
            decoded_line
            .replace("\t", "")
            .replace("\r", "")
            .replace("\n", "")
            .split(" ")
        )
    cantidad_votantes = 1000
    cantidad_candidatos = 100
    for i in range(cantidad_votantes):
        r = random.randint(0, len(nombres))
        n = nombres[r]
        nombres.remove(n)
        crearVotante(
            i,
            n[0],
            n[-1],
            "CC",
            "G",
            "localidad"+str(random.choice(range(10))+1)
        )
    for i in range(cantidad_votantes, cantidad_votantes+cantidad_candidatos):
        r = random.randint(0, len(nombres))
        n = nombres[r]
        nombres.remove(n)
        crearCandidato(
            i,
            n[0],
            n[-1],
            "CC",
            "partido"+str(random.choice(range(5))+1),
            "localidad"+str(random.choice(range(10))+1)
        )
    return redirect("/")


@app.route("/resumen-votacion")
def votacion_resumen():
    votosContados = contadorVotos()
    return render_template("votacion/resumen.html", votosContados=json.dumps(votosContados))


@app.route("/votacion/<string:id>")
def votacion_index(id):
    ha_votado = consultarSiHaVotado(id)
    votante = buscarPersona(id)
    candidatos = buscarCandidatosLocalidad(votante)
    db.commit()
    return render_template(
        "votacion/index.html",
        ha_votado=ha_votado,
        votante=votante,
        candidatos=candidatos
    )


@app.route("/votacion/transaccion/<string:id>", methods=['POST'])
def votacion_transaccion(id):
    _id_candidato = request.form["eleccion"]
    _id_votante = id
    crearVoto(_id_votante, _id_candidato)
    return redirect("/")


@app.route("/votante")
def votante_index():
    votantes = obtenerVotantes()
    votaciones = obtenerVotaciones()
    db.commit()
    return render_template(
        "votantes/index.html",
        votantes=votantes,
        votaciones=votaciones,
        votacionesjson=json.dumps(votaciones)
    )


@app.route("/votante/buscar/<string:busqueda>")
def votante_busqueda(busqueda=""):
    votantes = buscarVotante(busqueda)
    return render_template("votantes/index.html", votantes=votantes, busqueda=busqueda)


@app.route('/votante/eliminar/<string:id>')
def votante_eliminar(id):
    eliminarVotante(id)
    return redirect("/votante")


@app.route('/votante/editado', methods=['POST'])
def votante_editado():
    actualizarVotante(
        request.form["id"],
        request.form["nombre"],
        request.form["apellido"],
        request.form["tipodoc"],
        request.form["genero"],
        request.form["localidad"]
    )
    return redirect("/votante")


@app.route('/votante/crear')
def votante_create():
    return render_template("votantes/crear.html")


@app.route('/votante/creado', methods=['POST'])
def votante_creado():
    crearVotante(
        request.form["id"],
        request.form["nombre"],
        request.form["apellido"],
        request.form["tipodoc"],
        request.form["genero"],
        request.form["localidad"]
    )
    return redirect("/votante")


@app.route("/candidato")
def candidato_index():
    candidatos = obtenerCandidatos()
    votaciones = obtenerVotaciones()
    return render_template("candidatos/index.html", candidatos=candidatos, votaciones=votaciones, votacionesjson=json.dumps(votaciones))


@app.route("/candidato/buscar/<string:busqueda>")
def candidato_busqueda(busqueda=""):
    candidatos = buscarCandidato(busqueda)
    return render_template("candidatos/index.html", candidatos=candidatos, busqueda=busqueda)


@app.route('/candidato/eliminar/<string:id>')
def candidato_eliminar(id):
    eliminarCandidato(id)
    return redirect("/candidato")


@app.route('/candidato/editado', methods=['POST'])
def candidato_editado():
    actualizarCandidato(
        request.form["id"],
        request.form["nombre"],
        request.form["apellido"],
        request.form["tipodoc"],
        request.form["partido"],
        request.form["localidad"]
    )
    return redirect("/candidato")


@app.route('/candidato/creado', methods=['POST'])
def candidato_creado():
    crearCandidato(
        request.form["id"],
        request.form["nombre"],
        request.form["apellido"],
        request.form["tipodoc"],
        request.form["partido"],
        request.form["localidad"]
    )
    return redirect("/candidato")


app.run(debug=True, host="0.0.0.0")
