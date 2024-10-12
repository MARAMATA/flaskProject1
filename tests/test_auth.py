import json

def test_login(client, init_database):
    """
    Test de la route POST /auth/login pour connecter un utilisateur.
    """
    login_data = {
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    response = client.post('/auth/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'token' in data

def test_login_invalid_password(client, init_database):
    """
    Test de la route POST /auth/login avec un mot de passe incorrect.
    """
    login_data = {
        'email': 'testuser@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/auth/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 401
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'Login ou mot de passe incorrect !'

def test_access_protected_route_without_token(client):
    """
    Test d'accès à une route protégée sans fournir de jeton.
    """
    response = client.get('/users')
    assert response.status_code == 403
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'Jeton manquant !'
