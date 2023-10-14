from app import db, login_manager
from itsdangerous import TimedSerializer
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'User(id={self.id}, email:{self.email})'

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default='untitled note')
    content = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # last_updated = db.Column(db.DateTime, nullable=False, default=datetime.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Model(id={self.id}, title={self.email}, content={self.content[0:50]}...)'
