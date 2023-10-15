import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_URL = 'sqlite:///' + os.path.join(basedir, 'app.db')


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
