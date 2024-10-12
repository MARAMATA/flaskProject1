import pytest

def test_home_route(client):
    """
    Test de la route GET / pour vérifier que la page d'accueil fonctionne.
    """
    response = client.get('/')
    assert response.status_code == 200

def test_swagger_route(client):
    """
    Test de la route GET /swaggerfile pour vérifier que Swagger fonctionne.
    """
    response = client.get('/swaggerfile')
    assert response.status_code == 200

