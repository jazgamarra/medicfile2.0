from flask import Flask, render_template, url_for, redirect, request 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime, date 

# Creamos la aplicacion
app = Flask(__name__)

# Conectar a la base de datos que creamos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SECRET_KEY'] = 'secret_key!'

# Crear la base de datos
db = SQLAlchemy(app)

# Crear el objeto de encriptacion
bcrypt = Bcrypt(app)

# Configurar el login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Cargar el usuario actual de la sesion actual
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id)) 

# Modelo de tabla para la base de datos de usuarios 
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False) 

class Ficha (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False) 
    apellido = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    nacionalidad = db.Column(db.String(50), nullable=False)
    grupo_sanguineo = db.Column(db.String(50), nullable=False)
    alergias = db.Column(db.String(50), nullable=False)
    enfermedades = db.Column(db.String(50), nullable=False)
    medicamentos = db.Column(db.String(50), nullable=False)
    medico_cabecera = db.Column(db.String(50), nullable=False)
    seguro_medico = db.Column(db.String(50), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

# Crear tablas en sql alchemy 
with app.app_context():
    db.create_all()

def calcular_edad(fecha_nacimiento):
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
    today = date.today()
    edad = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad 

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Guardamos los datos de inicio de sesion 
        document = request.form.get('nro_documento')
        password = request.form.get('password')

        # Buscamos el usuario en la base de datos
        user = Users.query.filter_by(document=document).first() 
        if user is not None:
           # Comparamos la contraseña ingresada con la de la base de datos 
            if bcrypt.check_password_hash(user.password, password): 
                login_user(user)
                return 'success'
            else:
                return "warning contraseña incorrecta"
        else:
            return "warning usuario no encontrado"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Guardamos los datos de inicio de sesion 
        document = request.form.get('nro_documento')
        password = request.form.get('password')
        password2 = request.form.get('password2') 
        if password == password2: 
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            user = Users(document=document, password=password_hash)
            db.session.add(user)
            db.session.commit()
            login_user(user) 
        else: 
            return "warning contraseña no coincide"
        return redirect(url_for('crear_ficha'))
    return render_template('register.html')

@app.route('/crear_ficha', methods=['GET', 'POST'])
def crear_ficha():
    if request.method == 'POST':

        # Guardamos los datos de inicio de sesion 
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        nacionalidad = request.form.get('nacionalidad')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        grupo_sanguineo = request.form.get('grupo_sanguineo')
        alergias = request.form.get('alergias')
        enfermedades = request.form.get('enfermedades')
        medicamentos = request.form.get('medicamentos')
        medico_cabecera = request.form.get('medico')
        seguro_medico = request.form.get('seguro')

        id_user = current_user.id 
        edad = calcular_edad(fecha_nacimiento)

        # Creamos la ficha
        ficha = Ficha(id_user=id_user, nombre=nombre, apellido=apellido, nacionalidad=nacionalidad, grupo_sanguineo=grupo_sanguineo, alergias=alergias, enfermedades=enfermedades, medicamentos=medicamentos, medico_cabecera=medico_cabecera, seguro_medico=seguro_medico, edad=edad) 

        # Guardamos la ficha en la base de datos
        db.session.add(ficha)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('crear_ficha.html') 

if __name__ == '__main__':
    app.run(debug=True) 