import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

    # Utiliser PostgreSQL pour SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'postgresql://default_user:default_pass@localhost:5432/default_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

