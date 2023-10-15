from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, DateField,  SubmitField,
    SelectField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


class CategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired()])
    submit = SubmitField('Add category')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in ')


class NoteForm(FlaskForm):
    header = StringField('Header', validators=[DataRequired()])
    text = TextAreaField('Note text', validators=[DataRequired()])
    expires_on = DateField(
        'Expires on', format='%Y-%m-%d', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)
    submit = SubmitField('Add Note')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please enter a different name')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please enter a different email')
