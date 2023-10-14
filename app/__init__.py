from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '6d7d8936e9cfb34a7619c92021c95f55'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notesapp.db'

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app.notes.routes import notes
from app.users.routes import users
from app.errors.handlers import errors

app.register_blueprint(notes)
app.register_blueprint(users)
app.register_blueprint(errors)

