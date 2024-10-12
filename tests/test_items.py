import json
from app.models import Item, User

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

def test_create_item(client, init_database):
    """
    Test de la route POST /items pour créer un nouvel item.
    """
    token = get_token(client)
    new_item = {
        'name': 'item1',
        'description': 'A test item',
        'user_id': 1
    }
    response = client.post('/items', data=json.dumps(new_item), content_type='application/json', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201

def test_get_items(client, init_database):
    """
    Test de la route GET /items pour récupérer tous les items.
    """
    token = get_token(client)
    response = client.get('/items', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_get_item(client, init_database):
    """
    Test de la route GET /items/<id> pour récupérer un item spécifique.
    """
    token = get_token(client)
    response = client.get('/items/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_update_item(client, init_database):
    """
    Test de la route PUT /items/<id> pour mettre à jour un item.
    """
    token = get_token(client)
    updated_data = {
        'name': 'updated_item'
    }
    response = client.put('/items/1', data=json.dumps(updated_data), content_type='application/json', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_delete_item(client, init_database):
    """
    Test de la route DELETE /items/<id> pour supprimer un item.
    """
    token = get_token(client)
    response = client.delete('/items/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
