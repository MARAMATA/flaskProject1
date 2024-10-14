import os

class Config:

    SECRET_KEY = ''

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'postgresql://default_user:default_pass@localhost:5432/default_db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

