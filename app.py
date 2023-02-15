from flask import Flask, render_template, url_for, redirect 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt

# Creamos la aplicacion
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Conectar a la base de datos que creamos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SECRET_KEY'] = 'secret_key!'

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
    username = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

# Clase SignupForm para crear el formulario de registro de usuarios nuevos
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Nombre de usuario"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Contrasenha"})
    submit = SubmitField('Crear cuenta')

# Clase LoginForm para crear el formulario de inicio de sesion de usuarios existentes 
class LoginForm (FlaskForm):
    id = StringField('Id', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField('Iniciar sesion')

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/login', methods=['GET',    'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit(): 
        print ("login del usuario:"+form.username.data) 

    return render_template('login.html', form=form)