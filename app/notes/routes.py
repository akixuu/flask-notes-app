from flask import Blueprint, render_template, redirect, url_for

notes = Blueprint('notes', __name__)

@notes.route("/")
def view_notes():
    return render_template('home.html', title = 'Home')

@notes.route("/note/create", methods=["GET", "POST"])
def create_note():
    return render_template('base.html')

@notes.route("/note/<id>/edit", methods=["GET", "POST"])
def edit_note(id):
    return render_template('base.html')

@notes.route("/note/<id>/delete")
def delete_note(id):
    return render_template('base.html')