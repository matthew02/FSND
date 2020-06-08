"""Flask config class."""

import os


class Config(object):
    """Sets Flask configuration variables."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_LENGTH = 5


class ProductionConfig(Config):
    """Sets Flask configuration variables for the production environment."""


class DevelopmentConfig(Config):
    """Sets Flask configuration variables for the development environment."""
    SECRET_KEY = 'dev'
    DEBUG = 'true'
    FLASK_ENV = 'development'
    #HOST = '0.0.0.0'
    SERVER_NAME = 'pythondev.local:5000'
    SQLALCHEMY_DATABASE_URI = 'postgres://jsmith@localhost:5432/trivia'


class TestingConfig(Config):
    """Sets Flask configuration variables for the testing environment."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
