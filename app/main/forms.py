from flask_wtf import FlaskForm
from wtforms import (
    StringField, DateField,  SubmitField,
    SelectField, TextAreaField)
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired()])
    submit = SubmitField('Add category')


class NoteForm(FlaskForm):
    header = StringField('Header', validators=[DataRequired()])
    text = TextAreaField('Note text', validators=[DataRequired()])
    expires_on = DateField(
        'Expires on', format='%Y-%m-%d', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)
    submit = SubmitField('Add Note')
