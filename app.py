from flask import Flask, render_template, request, redirect, flash, url_for,  get_flashed_messages
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, static_url_path='/static')

load_dotenv()

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# Configuración de Flask-Login
app.secret_key = "mysecretkey"
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."
login_manager.login_message_category = "warning"

# Definición del modelo de usuario
class User(UserMixin):
    def __init__(self, id, nombre, email, password):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, email, contraseña FROM usuario WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

# Ruta para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['contraseña']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, email, contraseña FROM usuario WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[3], password):
            user_obj = User(user[0], user[1], user[2], user[3])
            login_user(user_obj)
            flash('Inicio de sesión exitoso!', 'success')
            return redirect(url_for('enologo'))
        else:
            flash('Usuario y Contraseña incorrecta', 'error')
            return redirect(url_for('register'))
        
    return render_template('login.html')

# Ruta para registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Formulario enviado")
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['contraseña']

        # Genera el hash de las contraseñas
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (nombre, email, contraseña) VALUES (%s, %s, %s)", (nombre, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registro exitoso, ahora puedes iniciar sesión', 'success')
        print("Redireccionando a login")
        return redirect(url_for('login'))
    
    return render_template('register.html')

#ruta para proteger autentificacion
@app.route('/protected')
@login_required
def protected():
    return "Esta es una página protegida, solo visible para usuarios logeados."


@app.route('/')
def main():
    return render_template('index.html')

#@app.route('/enologo')
#def enologo():
#    return render_template('enologo.html')

@app.route('/enologo', methods=['GET', 'POST'])
def enologo():
    if request.method == 'POST':
        vigencia  = request.form['vigencia']
        revision  = request.form['revision']
        fecha  = request.form['fecha']
        laboratorio   = request.form['laboratorio']
        vinoMosto = request.form['vinoMosto']
        codigo = request.form['codigo']
        densidad = request.form['densidad']
        extDens = request.form['extDens']
        bx = request.form['bx']
        alcAlcolyzer = request.form['alcAlcolyzer']
        alcDest = request.form['alcDest']
        azQco = request.form['azQco']
        foss = request.form['foss']
        so2lt = request.form['so2lt']
        so2Real = request.form['so2Real']
        so2Rankine = request.form['so2Rankine']
        atTitulable = request.form['atTitulable']
        avDestilacion = request.form['avDestilacion']
        colorEspectro = request.form['colorEspectro']
        oxigeno = request.form['oxigeno']
        co2 = request.form['co2']
        rcih = request.form['rcih']
        rProtCalor = request.form['rProtCalor']
        hierro = request.form['hierro']
        cobre = request.form['cobre']
        potasio = request.form['potasio']
        sorbato = request.form['sorbato']
        purezaVarietal = request.form['purezaVarietal']
        matColArt = request.form['matColArt']
        calcio = request.form['calcio']
        cloruros = request.form['cloruros']
        sulfatos = request.form['sulfatos']
        ferro = request.form['ferro']
        checkStab = request.form['checkStab']
        filtrabilidad = request.form['filtrabilidad']
        pruebaFrio = request.form['pruebaFrio']
        npa = request.form['npa']
        polifTotales = request.form['polifTotales']
        rtoViabilidad = request.form['rtoViabilidad']
        ntu = request.form['ntu']
        
                # Convertir a enteros si es posible, de lo contrario asignar None o un valor por defecto
        try:
            revision = int(revision) if revision.isdigit() else None
            codigo = int(codigo) if codigo.isdigit() else None
        except ValueError:
            revision = None
            codigo = None


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO solicitudMuestra (vigencia, revision, fecha, laboratorio, vinoMosto, codigo, densidad, extDens, bx, alcAlcolyzer, alcDest, azQco, foss, so2lt, so2Real, so2Rankine, atTitulable, avDestilacion, colorEspectro, oxigeno, co2, rcih, rProtCalor, hierro, cobre, potasio, sorbato, purezaVarietal, matColArt, calcio, cloruros, sulfatos, ferro, checkStab, filtrabilidad, pruebaFrio, npa, polifTotales, rtoViabilidad, ntu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (vigencia, revision, fecha, laboratorio, vinoMosto, codigo, densidad, extDens, bx, alcAlcolyzer, alcDest, azQco, foss, so2lt, so2Real, so2Rankine, atTitulable, avDestilacion, colorEspectro, oxigeno, co2, rcih, rProtCalor, hierro, cobre, potasio, sorbato, purezaVarietal, matColArt, calcio, cloruros, sulfatos, ferro, checkStab, filtrabilidad, pruebaFrio, npa, polifTotales, rtoViabilidad, ntu))
        mysql.connection.commit()
        cur.close()
        
        flash('Registro exitoso, ahora puedes iniciar sesión', 'success')
        print("Redireccionando a login")
        return redirect(url_for('enologo'))
    
    return render_template('enologo.html')

# ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('main'))

@app.route('/laboratorio')
def laboratorio():
    # Crear el cursor y ejecutar la consulta para obtener los datos de solicitudMuestra
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM solicitudMuestra")
    datos = cur.fetchall()  # Obtener todos los datos de la consulta
    cur.close()
    
    return render_template('laboratorio.html', datos=datos)

@app.route('/enviar_muestra', methods=['POST'])
def enviar_muestra():
    if request.method == 'POST':
        vigencia  = request.form['vigencia']
        revision  = request.form['revision']
        fecha  = request.form['fecha']
        laboratorio   = request.form['laboratorio']
        vinoMosto = request.form['vinoMosto']
        codigo = request.form['codigo']
        densidad = request.form['densidad']
        extDens = request.form['extDens']
        bx = request.form['bx']
        alcAlcolyzer = request.form['alcAlcolyzer']
        alcDest = request.form['alcDest']
        azQco = request.form['azQco']
        foss = request.form['foss']
        so2lt = request.form['so2lt']
        so2Real = request.form['so2Real']
        so2Rankine = request.form['so2Rankine']
        atTitulable = request.form['atTitulable']
        avDestilacion = request.form['avDestilacion']
        colorEspectro = request.form['colorEspectro']
        oxigeno = request.form['oxigeno']
        co2 = request.form['co2']
        rcih = request.form['rcih']
        rProtCalor = request.form['rProtCalor']
        hierro = request.form['hierro']
        cobre = request.form['cobre']
        potasio = request.form['potasio']
        sorbato = request.form['sorbato']
        purezaVarietal = request.form['purezaVarietal']
        matColArt = request.form['matColArt']
        calcio = request.form['calcio']
        cloruros = request.form['cloruros']
        sulfatos = request.form['sulfatos']
        ferro = request.form['ferro']
        checkStab = request.form['checkStab']
        filtrabilidad = request.form['filtrabilidad']
        pruebaFrio = request.form['pruebaFrio']
        npa = request.form['npa']
        polifTotales = request.form['polifTotales']
        rtoViabilidad = request.form['rtoViabilidad']
        ntu = request.form['ntu']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO solicitudMuestra (vigencia, revision, fecha, laboratorio, vinoMosto, codigo, densidad, extDens, bx, alcAlcolyzer, alcDest, azQco, foss, so2lt, so2Real, so2Rankine, atTitulable, avDestilacion, colorEspectro, oxigeno, co2, rcih, rProtCalor, hierro, cobre, potasio, sorbato, purezaVarietal, matColArt, calcio, cloruros, sulfatos, ferro, checkStab, filtrabilidad, pruebaFrio, npa, polifTotales, rtoViabilidad, ntu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (vigencia, revision, fecha, laboratorio, vinoMosto, codigo, densidad, extDens, bx, alcAlcolyzer, alcDest, azQco, foss, so2lt, so2Real, so2Rankine, atTitulable, avDestilacion, colorEspectro, oxigeno, co2, rcih, rProtCalor, hierro, cobre, potasio, sorbato, purezaVarietal, matColArt, calcio, cloruros, sulfatos, ferro, checkStab, filtrabilidad, pruebaFrio, npa, polifTotales, rtoViabilidad, ntu))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/laboratorio')


if __name__ == "__main__":
    app.run(port=5020, debug=True)