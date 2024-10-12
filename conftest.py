import pytest
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:passer@localhost:5432/API_FLASK_TEST'  # Base de test

    with app.app_context():
        db.create_all()  # Crée toutes les tables nécessaires avant les tests
        yield app
        db.drop_all()  # Nettoie la base de données après les tests

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        # Ajout de données initiales de test
        user = User(username='testuser', email='testuser@example.com', password_hash=generate_password_hash('password123'))
        db.session.add(user)
        db.session.commit()
        yield db
        db.session.remove()
        db.drop_all()  # Supprime toutes les tables après chaque test
