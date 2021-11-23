import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="prueba"
)

cursor = db.cursor()

cursor.execute("DROP FUNCTION IF EXISTS HA_VOTADO")

cursor.execute('''
        CREATE FUNCTION HA_VOTADO(_id_persona TEXT) RETURNS BOOLEAN
            BEGIN
                IF EXISTS (SELECT _id_votante FROM votacion WHERE _id_votante=_id_persona) THEN
                    RETURN TRUE;
                END IF;
                RETURN FALSE;
            END
''')


def crearTabla(nombreTabla, estructura):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS "+nombreTabla+"("
        + estructura +
        ")"
    )
    db.commit()
    print("Tabla creada: " + nombreTabla)


def borrarTabla(nombreTabla):
    cursor.execute(
        "DROP TABLE IF EXISTS "+nombreTabla
    )
    db.commit()
    print("Tabla eliminada: " + nombreTabla)


def crearVotante(id, nombre, apellido, tipodoc, genero, localidad):
    sql = '''
    IF NOT EXISTS(SELECT * FROM `votante` WHERE `_id`=%s) THEN 
        INSERT INTO `votante` (`_id`, `nombre`, `apellido`, `tipodoc`,`genero`, `localidad`) VALUES (%s, %s, %s, %s, %s, %s);
    END IF;
    '''
    cursor.execute(
        sql, (id, id, nombre, apellido, tipodoc, genero, localidad)
    )
    db.commit()


def actualizarVotante(id, nombre, apellido, tipodoc, genero, localidad):
    sql = '''
    IF EXISTS(SELECT * FROM votante WHERE _id=%s) THEN 
        UPDATE votante SET nombre=%s,apellido=%s,tipodoc=%s,genero=%s,localidad=%s WHERE _id=%s;
    END IF;
    '''
    cursor.execute(
        sql, (id, nombre, apellido, tipodoc, genero, localidad, id)
    )
    db.commit()


def actualizarCandidato(id, nombre, apellido, tipodoc, partido, localidad):
    sql = '''
    IF EXISTS(SELECT * FROM candidato WHERE _id=%s) THEN 
        UPDATE candidato SET nombre=%s,apellido=%s,tipodoc=%s,partido=%s,localidad=%s WHERE _id=%s;
    END IF;
    '''
    cursor.execute(
        sql, (id, nombre, apellido, tipodoc, partido, localidad, id)
    )
    db.commit()


def borrar_datos_tabla(tabla):
    sql = "DELETE FROM "+tabla+";"
    cursor.execute(sql)
    db.commit()


def crearCandidato(id, nombre, apellido, tipodoc, partido, localidad):
    sql = '''
    IF NOT EXISTS(SELECT * FROM `candidato` WHERE `_id`=%s) THEN 
        INSERT INTO `candidato` (`_id`, `nombre`, `apellido`, `tipodoc`, `partido`, `localidad`) VALUES (%s, %s, %s, %s, %s, %s);
    END IF;
    '''
    cursor.execute(
        sql, (id, id, nombre, apellido, tipodoc, partido, localidad)
    )
    db.commit()


def crearVoto(_id_votante, _id_candidato):
    sql = '''
    IF NOT EXISTS(SELECT * FROM votacion WHERE _id_votante=%s) THEN 
        INSERT INTO votacion (_id_votante, _id_candidato) VALUES (%s, %s);
    END IF;
    '''
    cursor.execute(
        sql, (_id_votante, _id_votante, _id_candidato)
    )
    db.commit()


def contadorVotos():
    sql = '''
    SELECT 
        (SELECT CONCAT(nombre," ",apellido) FROM candidato WHERE _id=_id_candidato),
        (SELECT localidad FROM candidato WHERE _id=_id_candidato) AS _localidad, 
        COUNT(*) AS n_votos FROM votacion 
    GROUP BY 
        _id_candidato 
        HAVING COUNT(*)>0 
    ORDER BY _localidad, n_votos DESC;  
    '''
    cursor.execute(sql)
    respuesta = cursor.fetchall()
    db.commit()
    return respuesta


def consultarSiHaVotado(id):
    sql = 'SELECT HA_VOTADO({0})'.format(id)
    cursor.execute(sql)
    respuesta = cursor.fetchone()
    db.commit()
    return respuesta[0] == 1


def buscarPersona(id):
    sql = 'SELECT * FROM votante WHERE _id={0}'.format(id)
    cursor.execute(sql, (id))
    respuesta = cursor.fetchone()
    votante = respuesta
    if not votante:
        sql = "SELECT * FROM candidato WHERE _id={0}".format(id)
        cursor.execute(sql, (id))
        respuesta = cursor.fetchone()
        votante = respuesta
    db.commit()
    return votante


def buscarCandidatosLocalidad(votante):
    sql = "SELECT * FROM candidato WHERE localidad='{0}'".format(votante[-1])
    print(sql)
    cursor.execute(sql)
    respuesta = cursor.fetchall()
    db.commit()
    return respuesta


def obtenerVotantes():
    sql = '''
    SELECT * FROM votante ORDER BY CAST(_id as int)
    '''
    cursor.execute(sql)
    votantes = cursor.fetchall()
    db.commit()
    return votantes


def obtenerCandidatos():
    sql = '''
    SELECT * FROM candidato ORDER BY CAST(_id as int)
    '''
    cursor.execute(sql)
    candidatos = cursor.fetchall()
    db.commit()
    return candidatos


def obtenerVotaciones():
    sql = '''
    SELECT _id_votante FROM votacion
    '''
    cursor.execute(sql)
    votaciones = cursor.fetchall()
    db.commit()
    return votaciones


def buscarVotante(busqueda):
    sql = '''
    SELECT * FROM votante WHERE _id = %s OR nombre = %s OR apellido = %s;
    '''
    cursor.execute(sql, (busqueda, busqueda, busqueda))
    votantes = cursor.fetchall()
    db.commit()
    return votantes


def buscarCandidato(busqueda):
    sql = '''
    SELECT * FROM candidato WHERE _id = %s OR nombre = %s OR apellido = %s;
    '''

    cursor.execute(sql, (busqueda, busqueda, busqueda))
    candidatos = cursor.fetchall()
    db.commit()
    return candidatos


def eliminarVotante(id):
    sql = '''
    DELETE FROM `votante` WHERE _id=%s
    '''
    cursor.execute(sql, (id))
    db.commit()

def eliminarCandidato(id):
    sql = '''
    DELETE FROM candidato WHERE _id=%s
    '''
    cursor.execute(sql, (id))
    db.commit()