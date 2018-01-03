import os


class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:P@$$w0rd@localhost:5432/blogful"
    DEBUG = True
