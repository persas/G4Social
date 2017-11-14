from flask import Flask, url_for
from flask import render_template
from flask import request
from flask import make_response
from flaskext.mysql import MySQL
import MySQLdb
from werkzeug.utils import redirect
import gastos
import unicodedata

app = Flask(__name__, template_folder='templates')
con = MySQLdb.connect(host="localhost", user="root", passwd="", db="gamejam")

mysql = MySQL
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'gamejam'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)


@app.route('/')
def showSignUp():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def signup():

    nombre = str(request.form["nombre"])
    password = str(request.form["password"])
    email = str(request.form["email"])
    apellido = str(request.form["apellido"])
    fechanacimiento = str(request.form["fechanacimiento"])
    genero = str(request.form["genre"])
    cursor = con.cursor()

    cursor.execute("INSERT INTO users (name, password , email, apellido, fechanacimiento ,genero,configuracioninicial) VALUES (%s,%s,%s,%s,%s,%s,0)",(nombre,password,email,apellido,fechanacimiento,genero))
    con.commit()

    response = make_response(check())
    return response

@app.route("/checkuser", methods=['POST'])
def check():
    password = str(request.form["password"])
    email = str(request.form["email"])
    cursor = con.cursor()
    cursor.execute("SELECT email  FROM users WHERE email ='" + email + "' AND password = '"+password+"'")
    email = cursor.fetchone()
    if email is None:
            return render_template("indexerror.html")
    else:
        if len(email) is 1:
            email = str(request.form["email"])
            cursor2 = con.cursor()
            cursor2.execute("SELECT name FROM users WHERE email ='" + email + "'")
            registro = cursor2.fetchone()
            nombre = registro[0].capitalize()

            cursor3 = con.cursor()
            cursor3.execute("SELECT configuracioninicial FROM users WHERE email ='" + email + "'")
            registro2 = cursor3.fetchone()
            configinicial = registro2[0]

            if configinicial is 0:
                response = make_response(render_template("/PrimerosPasos/index.html", nombreusuario=nombre))
                response.set_cookie('email', email)
                return response
            else:
                cursor = con.cursor()
                print (email)
                print(type(email))

                cursor.execute("SELECT gastos.gasto FROM gastos WHERE gastos.email = '" + email + "' AND gastos.principal = 1")
                gasto = cursor.fetchone()
                gasto = gasto[0]

                cursor.execute("SELECT reto FROM gastos WHERE gastos.email = '" + email + "' AND gastos.reto = 1")
                reto = cursor.fetchone()
                reto = reto[0]

                cursor.execute("SELECT ingreso FROM ingresos WHERE email = '" + email + "' AND ingresos.principal = 1")
                ingreso = cursor.fetchone()
                ingreso = ingreso[0]
                misgastos = gastos.calcula_gastos(ingreso, gasto, reto)

                cursor.execute("SELECT gasto FROM gastos WHERE email = '" + email + "'")
                resultadosgastos = cursor.fetchall()
                ahorro = ingreso
                for item in resultadosgastos:
                    ahorro = ahorro - item[0]

                cursor.execute("SELECT gasto FROM gastos WHERE gastos.email = '" + email + "' AND gastos.categoria = 'vivienda'")
                vivienda = cursor.fetchone()
                gastovivienda=0


                if vivienda is None:
                    gastovivienda = 0
                else:
                    for index in vivienda:
                        gastovivienda = gastovivienda + vivienda[0]

                cursor.execute("SELECT gasto FROM gastos WHERE gastos.email = '" + email + "' AND gastos.categoria = 'ocio'")
                ocio = cursor.fetchone()
                gastoocio = 0

                if ocio is None:
                    gastoocio = 0
                else:
                    for index in ocio:
                        gastoocio = gastoocio + ocio[0]

                cursor.execute("SELECT gasto FROM gastos WHERE gastos.email = '" + email + "' AND gastos.categoria = 'comida'")
                comida = cursor.fetchone()
                gastocomida = 0

                if comida is None:
                    gastocomida = 0
                else:
                    for index in comida:
                        gastocomida = gastocomida + comida[0]

                cursor.execute("SELECT gasto FROM gastos WHERE gastos.email = '" + email + "' AND gastos.categoria = 'otro'")
                otro = cursor.fetchone()
                gastootro = 0

                if otro is None:
                    gastootro = 0
                else:
                    for index in otro:
                        gastootro = gastootro + otro[0]


                gastosTotales = gastootro + gastocomida + gastoocio + gastovivienda

                print (gastosTotales)

                porcientoOtro = (gastootro * 100) / gastosTotales
                porcientoComida = (gastocomida *100 ) / gastosTotales
                porcientoOcio = (gastoocio * 100) / gastosTotales
                porcientoVivienda = (gastovivienda *100 ) / gastosTotales

                porcientoAhorro = ((ingreso-gastosTotales)*100)/ingreso

                response = make_response(
                    render_template("main/index.html",
                                    vivienda=gastovivienda, comida=gastocomida, ocio=gastoocio, otros=gastootro, ahorro=ahorro
                                    , porcientoComida = porcientoComida , porcientoOcio=porcientoOcio , porcientoOtro=porcientoOtro
                                    , porcientoVivienda=porcientoVivienda,porcientoAhorro=porcientoAhorro ))

                return response

        else:
            return render_template("indexerror.html")



@app.route("/reto", methods=['POST'])
def reto():

    email = request.cookies.get('email', 'Undefined')

    ingreso = int(request.form["ingreso"])
    gasto = int(request.form["gasto"])
    ahorro = int(request.form["ahorro"])


    cursor = con.cursor()

    cursor.execute("INSERT INTO ingresos (ingreso , tipo, principal, email) VALUES (%s,%s,1,%s)", (ingreso, 'nomina',email))
    cursor.execute("INSERT INTO gastos (gasto , categoria, principal, reto, tipogasto, gastos.email) VALUES (%s,%s,1,0,%s,%s)", (gasto, 'vivienda', 'fijo', email))
    cursor.execute("INSERT INTO gastos (gasto , categoria, principal, reto, tipogasto, gastos.email) VALUES (%s,%s,0,1,%s,%s)", (ahorro, 'ahorro', 'ahorro',email))

    con.commit()

    #response = make_response(render_template("/PrimerosPasos/index.html"))

    response = make_response(calc_gastos())
    cursor.execute("UPDATE users SET configuracioninicial=1 WHERE email='" + email + "'")
    con.commit()
    return response


@app.route("/gastos", methods=['POST'])
def calc_gastos():

    email = request.cookies.get('email')

    email2 = str(email)


    cursor = con.cursor()
    print (email2)
    print(type(email2))

    cursor.execute("SELECT gastos.gasto FROM gastos WHERE gastos.email = '" + email2 + "' AND gastos.principal = 1")
    gasto = cursor.fetchone()
    gasto = gasto[0]

    cursor.execute("SELECT reto FROM gastos WHERE gastos.email = '" + email2 + "' AND gastos.reto = 1")
    reto = cursor.fetchone()
    reto = reto[0]

    cursor.execute("SELECT ingreso FROM ingresos WHERE email = '" + email2 + "' AND ingresos.principal = 1")
    ingreso = cursor.fetchone()
    ingreso = ingreso[0]
    misgastos = gastos.calcula_gastos(ingreso, gasto, reto)

    cursor.execute("SELECT gasto FROM gastos WHERE email = '" + email2 + "'")
    resultado = cursor.fetchall()

    print(misgastos)

    ahorro = ingreso

    for item in resultado:
        ahorro = ahorro - resultado[0]

    response = make_response(render_template("main/index.html", vivienda=misgastos[0], comida=misgastos[1],casa=misgastos[2], ocio=misgastos[3], otros=misgastos[4], ahorro=ahorro))

    return response


@app.route("/main", methods=['POST'])
def principal():
    '''
    email = request.cookies.get('email', 'Undefined')
    cursor = con.cursor()

    gasto = cursor.execute("SELECT gasto FROM gastos WHERE gastos.email = '" + email + "' AND gastos.principal = " + 1)
    reto = cursor.execute("SELECT reto FROM gastos WHERE gastos.email = '" + email + "'")

    ingreso = cursor.execute("SELECT ingreso FROM ingresos WHERE ingresos.email = '" + email + "' AND ingresos.principal = " + 1)

    misgastos = gastos.calcula_gastos(ingreso,gasto,reto)
    print
    '''
    response = make_response(showSignUp())

    return response


if __name__ == '__main__':
    app.run(debug=True, port=8000)