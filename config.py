DATABASE_URL = "postgresql://postgres:fr132456@localhost/medlabs_db?client_encoding=utf8"

class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False


