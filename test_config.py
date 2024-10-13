"""import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class TestConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

    # Utilisation de la base de données de test API_FLASK_TEST
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL',
                                        'postgresql://default_user:default_pass@localhost:5432/API_FLASK_TEST')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True  # Active le mode test pour Flask"""


