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
                #response = make_response(render_template("index.html"))
                #response.set_cookie('nombre', nombre)
                response = make_response(principal())
                response.set_cookie('nombre', nombre)
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

    cursor.execute("INSERT INTO ingresos (ingreso , tipo, principal, ingresos.email) VALUES (%s,%s,1,%s)", (ingreso, 'nomina',email))
    cursor.execute("INSERT INTO gastos (gasto , categoria, principal, reto, tipogasto, gastos.email) VALUES (%s,%s,1,0,%s,%s)", (gasto, 'vivienda', 'fijo', email))
    cursor.execute("INSERT INTO gastos (gasto , categoria, principal, reto, tipogasto, gastos.email) VALUES (%s,%s,0,1,%s,%s)", (ahorro, 'ahorro', 'ahorro',email))

    con.commit()

    #response = make_response(render_template("/PrimerosPasos/index.html"))
    response = make_response(calc_gastos())
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

    cursor.execute("SELECT ingreso FROM ingresos WHERE ingresos.email = '" + email2 + "' AND ingresos.principal = 1")
    ingreso = cursor.fetchone()
    ingreso = ingreso[0]

    response = make_response(render_template("/PrimerosPasos/index.html"))

    return response


@app.route("/main", methods=['POST'])
def principal():

    email = request.cookies.get('email', 'Undefined')
    cursor = con.cursor()

    gasto = cursor.execute("SELECT gasto FROM gastos WHERE gastos.email = '" + email + "' AND gastos.principal = " + 1)
    reto = cursor.execute("SELECT reto FROM gastos WHERE gastos.email = '" + email + "'")

    ingreso = cursor.execute("SELECT ingreso FROM ingresos WHERE ingresos.email = '" + email + "' AND ingresos.principal = " + 1)

    misgastos = gastos.calcula_gastos(ingreso,gasto,reto)
    response = make_response(showSignUp())

    return response



if __name__ == '__main__':
    app.run(debug=True, port=8000)