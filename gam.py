from flask import Flask, url_for
from flask import render_template
from flask import request
from flask import make_response
from flaskext.mysql import MySQL
import MySQLdb
from werkzeug.utils import redirect
import gastos

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

    cursor.execute("INSERT INTO users (name, password , email, apellido, fechanacimiento ,genero) VALUES (%s,%s,%s,%s,%s,%s)",(nombre,password,email,apellido,fechanacimiento,genero))
    con.commit()

    return redirect(url_for("showSignUp"))

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
            response = make_response(render_template("/PrimerosPasos/index.html", nombreusuario=nombre))
            response.set_cookie('nombre', nombre)
            return response
        else:
            return render_template("indexerror.html")

@app.route("/main", methods=['POST'])
def principal():
    cursor = con.cursor()
    #cursor.execute("SELECT ingreso FROM users WHERE")
    misgastos = gastos.calculagastos()

if __name__ == '__main__':
    app.run(debug=True, port=8000)