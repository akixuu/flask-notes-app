from app import db, login_manager, app
from itsdangerous import TimedSerializer
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedSerializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def get_recovery_token(self):
        s = TimedSerializer(app.config['SECRET_KEY'])
        return s.dumps(self.id)
    
    @staticmethod
    def validate_recovery_token(token):
        s = TimedSerializer(app.config['SECRET_KEY'])
        try:
            id = TimedSerializer.load(token, max_age=1800)
        except:
            return
        
        return User.query.get(id)
        



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
