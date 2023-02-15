from flask import Flask, render_template, url_for, redirect 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

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
    return User.query.get(int(user_id)) 

# Modelo de tabla para la base de datos de usuarios 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False) 

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True) 