from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app.users.forms import *
from app.models import User
from app import bcrypt, db, mail
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
                sender=current_app.config['MAIL_USERNAME'], 
                recipients=[form.email.data], 
                body=f'''Here is your password recovery link: {url_for('users.recovery', token=token, _external=True)}\n\n If you did not make this request then simply ignore this email and no changes will be made.''')
            mail.send(msg)
            return redirect(url_for('users.login'))
    return render_template('auth/recovery.html', title='Reset Password', form=form)


@users.route('/recovery/<token>', methods=['GET', 'POST'])
def recovery(token):
    if current_user.is_authenticated:
        return redirect(url_for('notes.view_notes'))
    
    user = User.validate_recovery_token(token)
    if user is None:
        flash(f'That is an invalid or expired token', 'warning')
        return redirect(url_for('users.recovery_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash(f'Password updated, please login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('auth/reset_password.html', title='Reset Password', form=form)

@users.route('/settings')
def settings():
    return ''
