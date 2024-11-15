from flask import Flask, render_template, request, redirect, flash, url_for,  get_flashed_messages
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector



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

#ruta login encargado
@app.route('/loginenc', methods=['GET', 'POST'])
def loginenc():
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
            return redirect(url_for('encargado'))
        else:
            flash('Usuario y Contraseña incorrecta', 'error')
            return redirect(url_for('register'))
        
    return render_template('loginencargado.html')

#ruta login laboratorio
@app.route('/loginb', methods=['GET', 'POST'])
def loginb():
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
            return redirect(url_for('laboratorio'))
        else:
            flash('Usuario y Contraseña incorrecta', 'error')
            return redirect(url_for('register'))
        
    return render_template('loginlaborat.html')

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

@app.route('/enologo')
def enologo():
    return render_template('enologo.html')

@app.route('/encargado')
def encargado():
    return render_template('encargado.html')

@app.route('/laboratorio')
def laboratorio():
    return render_template('laboratorio.html')


############################################################################



#PARA ENOLOGO VINOS EN PROCESO
#ruta vinos en proceso
@app.route('/vinosproceso')
def vinosproceso():
    return render_template('vinosproceso.html')


#ruta para cargar los archivos
@app.route('/cargar_datos')
@login_required
def cargar_datos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vinosproceso')
    data = cur.fetchall()
    return render_template( 'vinosproceso.html', clientes = data)


#lo nuevo ruta de save
@app.route('/save')
@login_required
def save():
    return render_template('save.html')



#rutas para agregar los archivos
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        print('Formulario enviado')
        tipodevino = request.form['tipodevino']
        variedaddeuva = request.form['variedaddeuva']
        numerovasija= request.form['numerovasija']
        metodosvinificacion= request.form['metodosvinificacion']
        cur = mysql.connection.cursor()
        print(f'Recibido: {tipodevino}, {variedaddeuva}, {numerovasija}, {metodosvinificacion}')
        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO vinosproceso (tipodevino, variedaddeuva, numerovasija, metodosvinificacion)
                    VALUES (%s, %s, %s, %s)'''
                    , (tipodevino, variedaddeuva, numerovasija, metodosvinificacion))
            mysql.connection.commit()
            cur.close()
            print('Datos insertados correctamente, redireccionando...')
            return redirect(url_for('cargar_datos'))
        except Exception as e:
            print(f'Error al insertar los datos: {e}')
            return render_template('vinosproceso.html')


# Rutas para editar los registros
@app.route('/edit/<id>')
def get_client(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vinosproceso WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editar.html',contact= data[0])


#ruta para actualizar los registros
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        tipodevino = request.form['tipodevino']
        variedaddeuva = request.form['variedaddeuva']
        numerovasija= request.form['numerovasija']
        metodosvinificacion= request.form['metodosvinificacion']
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE vinosproceso
            SET  tipodevino = %s, variedaddeuva = %s, numerovasija = %s, metodosvinificacion = %s
            WHERE id = %s'''
                , ( tipodevino, variedaddeuva, numerovasija, metodosvinificacion, id))
        mysql.connection.commit()
        return redirect(url_for('cargar_datos'))


#Ruta para eliminar registros
@app.route('/delete/<id>', methods=['POST'])
@login_required
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM vinosproceso WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    flash('Contacto eliminado exitosamente', 'success')
    return redirect(url_for('cargar_datos'))

# ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('main'))
#HASTA ACA

#######################################################33

#PARA ENCARGADO
#ruta ordenes de trabajo
@app.route('/ordenestrabajo')
def ordenestrabajo():
    return render_template('ordenestrabajo.html')

#lo nuevo ruta de save encargado
@app.route('/saveordenes')
@login_required
def saveordenes():
    return render_template('saveordenes.html')

#ruta para cargar los archivos encargado
@app.route('/cargar_datosordenes')
@login_required
def cargar_datosordenes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ordentrabajo')
    data = cur.fetchall()
    return render_template( 'ordenestrabajo.html', clientes = data)

#rutas para agregar los archivos de encargado
@app.route('/addordenes', methods=['POST'])
def addordenes():
    if request.method == 'POST':
        print('Formulario enviado')
        sector = request.form['sector']
        operario = request.form['operario']
        fecha= request.form['fecha']
        detalles_tarea = request.form['detalles_tarea']
        encargado_a_cargo = request.form['encargado_a_cargo']
        cur = mysql.connection.cursor()
        print(f'Recibido: {sector}, {operario}, {fecha}, {detalles_tarea}, {encargado_a_cargo}')
        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO ordentrabajo (sector, operario, fecha, detalles_tarea, encargado_a_cargo)
                    VALUES (%s, %s, %s, %s, %s)'''
                    , (sector, operario, fecha, detalles_tarea, encargado_a_cargo))
            mysql.connection.commit()
            cur.close()
            print('Datos insertados correctamente, redireccionando...')
            return redirect(url_for('cargar_datosordenes'))
        except Exception as e:
            print(f'Error al insertar los datos: {e}')
            return render_template('ordenestrabajo.html')

# Rutas para editar los registros para encargado
@app.route('/editordenes/<id>')
def get_clientordenes(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ordentrabajo WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editarordenes.html',contact= data[0])

#ruta para actualizar los registros para encargado
@app.route('/updateordenes/<id>', methods=['POST'])
def update_contactordenes(id):
    if request.method == 'POST':
        sector = request.form['sector']
        operario = request.form['operario']
        fecha= request.form['fecha']
        detalles_tarea = request.form['detalles_tarea']
        encargado_a_cargo = request.form['encargado_a_cargo']
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE ordentrabajo
            SET  sector = %s, operario = %s, fecha = %s, detalles_tarea = %s, encargado_a_cargo = %s
            WHERE id = %s'''
                , ( sector, operario, fecha, detalles_tarea, encargado_a_cargo , id))
        mysql.connection.commit()
        return redirect(url_for('cargar_datosordenes'))


#Ruta para eliminar registros para encargado
@app.route('/deleteordenes/<id>', methods=['POST'])
@login_required
def delete_contactordenes(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM ordentrabajo WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    flash('Contacto eliminado exitosamente', 'success')
    return redirect(url_for('cargar_datosordenes'))


# ruta de logout para encargado
@app.route('/logoutordenes')
@login_required
def logoutordenes():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('main'))
#HASTA ACA LLEGA LO DE ENCARGADO


#ruta para el formulario del laboratorio
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

# Ruta para procesar el formulario
@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        data = {
            'tipovino': request.form['tipovino'],
            'sectorproveniente': request.form['sectorproveniente'],
            'id': request.form['id'],
            'rcqln': request.form['rcqln'],
            'vigencia': request.form['vigencia'],
            'revision': request.form['revision'],
            'fecha': request.form['fecha'],
            'laboratorio': request.form['laboratorio'],
            'vinoMosto': request.form['vinoMosto'],
            'codigo': request.form['codigo'],
            'densidad': request.form['densidad'],
            'extDens': request.form['extDens'], 
            'bx': request.form['bx'],
            'alcAlcolyzer': request.form['alcAlcolyzer'],
            'alcDest': request.form['alcDest'],
            'azQco' : request.form['azQco'],
            'foss' : request.form['foss'],
            'so2lt' : request.form['so2lt'],
            'so2Real' : request.form['so2Real'],
            'so2Rankine' : request.form['so2Rankine'],
            'atTitulable' : request.form['atTitulable'],
            'avDestilacion' : request.form['avDestilacion'],
            'colorEspectro' : request.form['colorEspectro'],
            'oxigeno' : request.form['oxigeno'],
            'co2' : request.form['co2'],
            'rcih' : request.form['rcih'],
            'rProtCalor' : request.form['rProtCalor'],
            'hierro' : request.form['hierro'],
            'cobre' : request.form['cobre'],
            'potasio' : request.form['potasio'],
            'sorbato' : request.form['sorbato'],
            'purezaVarietal' : request.form['purezaVarietal'],
            'matColArt' : request.form['matColArt'],
            'calcio' : request.form['calcio'],
            'cloruros' : request.form['cloruros'],
            'sulfatos' : request.form['sulfatos'],
            'ferro' : request.form['ferro'],
            'checkStab' : request.form['checkStab'],
            'filtrabilidad' : request.form['filtrabilidad'],
            'pruebaFrio' : request.form['pruebaFrio'],
            'npa' : request.form['npa'],
            'polifTotales' : request.form['polifTotales'],
            'rtoViabilidad' : request.form['rtoViabilidad'],
            'ntu' : request.form['ntu'],
        }
        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO solicitudMuestra 
                ( tipovino,sectorproveniente,id, rcqln, vigencia, revision, fecha, laboratorio, vinoMosto, codigo, densidad, extDens, bx, 
                alcAlcolyzer, alcDest, azQco, foss, so2lt, so2Real, so2Rankine, atTitulable, avDestilacion, 
                colorEspectro, oxigeno, co2, rcih, rProtCalor, hierro, cobre, potasio, sorbato, purezaVarietal, 
                matColArt, calcio, cloruros, sulfatos, ferro, checkStab, filtrabilidad, pruebaFrio, npa, 
                polifTotales, rtoViabilidad, ntu)
                VALUES (%(tipovino)s,%(sectorproveniente)s,%(id)s,%(rcqln)s, %(vigencia)s, %(revision)s, %(fecha)s, %(laboratorio)s, %(vinoMosto)s, 
                %(codigo)s, %(densidad)s, %(extDens)s, %(bx)s, %(alcAlcolyzer)s, %(alcDest)s, %(azQco)s, 
                %(foss)s, %(so2lt)s, %(so2Real)s, %(so2Rankine)s, %(atTitulable)s, %(avDestilacion)s, 
                %(colorEspectro)s, %(oxigeno)s, %(co2)s, %(rcih)s, %(rProtCalor)s, %(hierro)s, %(cobre)s, 
                %(potasio)s, %(sorbato)s, %(purezaVarietal)s, %(matColArt)s, %(calcio)s, %(cloruros)s, 
                %(sulfatos)s, %(ferro)s, %(checkStab)s, %(filtrabilidad)s, %(pruebaFrio)s, %(npa)s, 
                %(polifTotales)s, %(rtoViabilidad)s, %(ntu)s)''', data)
            mysql.connection.commit()
            flash("Formulario enviado y datos guardados correctamente en la base de datos.", "success")
        except Exception as e:
            flash(f"Ocurrió un error al enviar el formulario: {e}", "error")
        finally:
            cur.close()
    return redirect(url_for('formulario'))


@app.route('/ver_formulario')
def ver_formulario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM solicitudMuestra")
    datos_formulario = cur.fetchall() 
    cur.close()

    return render_template('ver_formulario.html', datos_formulario=datos_formulario)

@app.route('/ver_detalle/<int:id>')
def ver_detalle(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM solicitudMuestra WHERE id = %s", (id,))
    detalle = cur.fetchone()
    cur.close()

    if detalle:
        return render_template('ver_detalle.html', detalle=detalle)
    else:
        flash("Formulario no encontrado.", "error")
        return redirect(url_for('ver_formulario'))


if __name__ == "__main__":
    app.run(port=5020, debug=True)