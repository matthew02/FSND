import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
FLASK_ENV = 'development'
SERVER_NAME = 'pythondev.local:5000'
SQLALCHEMY_DATABASE_URI = 'postgres://jsmith@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False
