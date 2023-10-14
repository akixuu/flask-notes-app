from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

notes = Blueprint('notes', __name__)

@login_required
@notes.route("/")
def view_notes():
    return render_template('home.html', title='Home')

# @login_required
# @notes.route("/note/create", methods=["GET", "POST"])
# def create_note():
#     return render_template('home.html')

# @login_required
# @notes.route("/note/<id>/edit", methods=["GET", "POST"])
# def edit_note(id):
#     return render_template('home.html')

# @login_required
# @notes.route("/note/<id>/delete")
# def delete_note(id):
#     return render_template('home.html')