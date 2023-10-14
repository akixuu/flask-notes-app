from flask import Flask

app = Flask(__name__)

from app.notes.routes import notes
from app.users.routes import users
from app.errors.handlers import errors

app.register_blueprint(notes)
app.register_blueprint(users)
app.register_blueprint(errors)

