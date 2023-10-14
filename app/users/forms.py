from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from app import db
from app.models import User

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me?')
    submit = SubmitField('Login')

class RegisterationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    password_matching = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already in use.')
        
class RecoverPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Send Recovery Code')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    password_matching = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Save New Password')
