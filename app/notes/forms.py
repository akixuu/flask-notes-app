from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class Note(FlaskForm):
    title = StringField('Title', validators=[Length(max=200)])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Finish')
    