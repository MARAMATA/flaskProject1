import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.from_object('test_config.TestConfig')  # Utilisation de la configuration de test

    with app.app_context():
        db.create_all()  # Crée les tables nécessaires avant les tests
        yield app
        db.drop_all()  # Nettoie la base de données après les tests

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database():
    with app.app_context():
        db.create_all()
        yield db  # Les tests peuvent utiliser cette base de données
        db.session.remove()
        db.drop_all()  # Nettoie la base après chaque test

def test_app_creation(app):
    assert app is not None
    assert app.config['TESTING']  # Assure-toi que l'application est en mode test
