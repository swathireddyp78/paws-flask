import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-secure-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/pawsdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME="localhost:6001"
    SESSION_COOKIE_DOMAIN="localhost:6001"