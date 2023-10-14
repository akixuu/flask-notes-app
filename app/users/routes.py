from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.users.forms import *
from app.models import User
from app import bcrypt, db, mail, app
from flask_login import current_user, login_user, logout_user
from flask_mail import Message

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('notes.view_notes'))
    
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hashing password
        user = User(email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Welcome! You have registered with your email {form.email.data}.', 'success')
        return redirect(url_for("notes.view_notes"))

    return render_template('auth/register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('notes.view_notes'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # password check
            login_user(user=user, remember=form.remember.data) # login
            flash(f'Logged in with email {form.email.data}.', category='info')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('notes.view_notes'))
        else: 
            flash(f'Login failed. Please check the email or password.', category='danger') 
        
    return render_template('auth/login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash(f'Logged out.', 'info')
    return redirect(url_for('users.login'))

@users.route('/recovery', methods=['GET', 'POST'])
def recovery_request():

    form = RecoverPasswordForm()
    if form.validate_on_submit():
        flash(f'If this email is associated with an account, we will send an recovery email shortly.', 'info')
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = User.get_recovery_token(user)
            msg = Message(
                subject='Password Recovery Link', 
                sender=app.config['MAIL_USERNAME'], 
                recipients=[form.email.data], 
                body=f'''Here is your password recovery link: {url_for('users.recovery', token=token, _external=True)} \n\nIf you did not request to reset your password, ignore this message.''')
            mail.send(msg)
            return redirect(url_for('users.login'))
    return render_template('auth/recovery.html', title='Reset Password', form=form)


@users.route('/recovery/<token>', methods=['GET', 'POST'])
def recovery(token):
    user_id = User.validate_recovery_token(token)
    if user_id is None:
        flash(f'The token is invalid or has expired. Please try again.')
        return redirect(url_for('users.recovery_request')) 
    
    user = User.query.get(user_id)
    if user is None:
        flash(f'The user for this password recovery no longer exists.')
        return redirect(url_for('users.login'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed
        db.session.commit()

        flash(f'Your password has been updated!')
        return redirect(url_for('users.login'))
    return render_template('auth/reset_password.html', title='Recovery', form=form)

@users.route('/settings')
def settings():
    return ''
