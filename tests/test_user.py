import json
from app.models import User

def get_token(client):
    """
    Fonction pour obtenir un jeton JWT après connexion.
    """
    login_data = {
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    response = client.post('/auth/login', data=json.dumps(login_data), content_type='application/json')
    return json.loads(response.data)['token']

def test_create_user(client, init_database):
    """
    Test de la route POST /users pour créer un nouvel utilisateur.
    """
    token = get_token(client)
    new_user = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    }
    response = client.post('/users', data=json.dumps(new_user), content_type='application/json', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201

def test_get_users(client, init_database):
    """
    Test de la route GET /users pour récupérer tous les utilisateurs.
    """
    token = get_token(client)
    response = client.get('/users', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_get_user(client, init_database):
    """
    Test de la route GET /users/<id> pour récupérer un utilisateur spécifique.
    """
    token = get_token(client)
    user = User.query.first()
    response = client.get(f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_update_user(client, init_database):
    """
    Test de la route PUT /users/<id> pour mettre à jour un utilisateur existant.
    """
    token = get_token(client)
    user = User.query.first()
    updated_data = {
        'username': 'updateduser',
        'email': 'updateduser@example.com'
    }
    response = client.put(f'/users/{user.id}', data=json.dumps(updated_data), content_type='application/json', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_delete_user(client, init_database):
    """
    Test de la route DELETE /users/<id> pour supprimer un utilisateur.
    """
    token = get_token(client)
    user = User.query.first()
    response = client.delete(f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
