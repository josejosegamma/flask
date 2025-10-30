import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
import os
DATABASE = os.path.join(os.path.dirname(__file__), "usuarios.db")


# -----------------------------
# FUNCIONES DE BASE DE DATOS
# -----------------------------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Crea la tabla y un usuario inicial"""
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        nombre TEXT, apellido TEXT, 
                        telefono TEXT, correo TEXT,
                        usuario TEXT UNIQUE,
                        clave TEXT
                    )''')
        # Insertar usuario por defecto si no existe
        c.execute("SELECT * FROM usuarios WHERE usuario = usuario")
        if not c.fetchone():
            c.execute("INSERT INTO usuarios (nombre, apellido, telefono, correo, usuario, clave) VALUES (?, ?, ?, ?, ?, ?)", ("Wilfer", "Hernandez", "3108346231", "wilfer@gmail.com", "admin", "1234"))
        conn.commit()




# -----------------------------
# RUTAS DE LA APLICACIÓN
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))
        user = cursor.fetchone()

        if user:
            return redirect(url_for("home", usuario=usuario))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template('login.html', error=error)

@app.route("/home")
def home():
    usuario = request.args.get("usuario", "Invitado")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")  
    datos = cursor.fetchall()
    conn.close()
    return render_template("home.html", usuarios=datos, usuario=usuario)

    

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    if request.method == 'POST':
        nombre=request.form['nombre']
        apellido=request.form['apellido']
        telefono=request.form['telefono']
        correo=request.form['correo']
        usuario=request.form['usuario']
        clave=request.form['clave']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, apellido, telefono, correo, usuario, clave) VALUES (?, ?, ?, ?, ?, ?)", (nombre, apellido, telefono, correo, usuario, clave))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("registro.html")



# -----------------------------
# EJECUCIÓN PRINCIPAL
# -----------------------------
if __name__ == "__main__":
    init_db()
    app.run()

