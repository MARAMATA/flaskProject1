import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir d'un fichier .env
load_dotenv()

class Config:

    SECRET_KEY = ''

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'postgresql://default_user:default_pass@localhost:5432/default_db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

