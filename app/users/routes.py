from flask import Blueprint, render_template, redirect, url_for

users = Blueprint('users', __name__)

@users.route('/register', methods=["GET", "POST"])
def register():
    return render_template('auth/register.html', title = 'Register')

@users.route('/login', methods=["GET", "POST"])
def login():
    return render_template('auth/login.html', title = 'Login')

@users.route('/logout')
def logout():
    return redirect(url_for('login'))

@users.route('/recovery', methods=["GET", "POST"])
def recovery():
    return render_template('auth/recovery.html', title = 'Recovery')

@users.route('/settings')
def delete_acc():
    return ''
