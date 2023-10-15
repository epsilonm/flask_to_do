from datetime import date, datetime

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __str__(self):
        return f'User {self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)      


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), index=True)
    notes = db.relationship('Note', backref='category', lazy='dynamic')


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    created_on = db.Column(db.DateTime(), index=True, default=datetime.now)
    expires_on = db.Column(db.Date())
    header = db.Column(db.String(128), index=True)
    text = db.Column(db.String(256))
    is_done = db.Column(db.Boolean(), default=False)
    user = db.relationship('User', backref=db.backref('notes', order_by=id))

    def __str__(self):
        return f'Note {self.header}'

    @hybrid_property
    def expired(self):
        if self.expires_on < date.today():
            return True
        return False

    def show_actual(self):
        pass


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
