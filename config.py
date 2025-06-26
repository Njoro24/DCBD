import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Application configuration class.

    This class holds all the configuration variables for the Flask application,
    such as database connection strings, secret keys, etc.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'devconnect.db')

  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-secret-key-that-should-be-stronger-in-prod'
