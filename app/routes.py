from flask import Blueprint, jsonify, request, abort, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Item
from .schemas import UserSchema, ItemSchema
from .auth import token_required, role_required, generate_token
from . import db

api_bp = Blueprint('api', __name__)

# Schémas de sérialisation
user_schema = UserSchema()
users_schema = UserSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# Route pour la page d'accueil
@api_bp.route('/')
def home():
    return render_template('index.html')

# ----------------- ROUTES UTILISATEURS -----------------

# Route GET pour récupérer tous les utilisateurs (ADMIN uniquement)
@api_bp.route('/users', methods=['GET'])
@token_required
@role_required('admin')  # Seuls les admins peuvent voir tous les utilisateurs
def get_users():
    users = User.query.all()
    if not users:
        abort(404, description="Aucun utilisateur trouvé")
    return jsonify(users_schema.dump(users)), 200

# Route GET pour récupérer un utilisateur spécifique (ADMIN et l'utilisateur lui-même)
@api_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="Utilisateur non trouvé")

    current_user = request.current_user
    if current_user.id != user.id and current_user.role != 'admin':
        abort(403, description="Accès refusé")

    return jsonify(user_schema.dump(user)), 200

# Route POST pour créer un nouvel utilisateur
@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validation des données
    if not data or not all(key in data for key in ['username', 'email', 'password', 'role']):
        abort(400, description="Données manquantes")

    # Vérification si un utilisateur avec le même username ou email existe déjà
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()

    if existing_user:
        if existing_user.username == data['username']:
            abort(400, description="Le nom d'utilisateur est déjà utilisé")
        if existing_user.email == data['email']:
            abort(400, description="L'adresse email est déjà utilisée")

    # Hachage du mot de passe
    hashed_password = generate_password_hash(data['password'])

    # Création d'un nouvel utilisateur
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        role=data['role']  # Utilisation du rôle fourni dans les données
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201

# Route PUT pour mettre à jour un utilisateur existant (L'utilisateur lui-même ou un admin)
@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    current_user = request.current_user

    if current_user.id != user.id and current_user.role != 'admin':
        abort(403, description="Accès refusé")

    data = request.get_json()

    if not data:
        abort(400, description="Aucune donnée fournie")

    errors = user_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    # Mettre à jour le mot de passe si fourni
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()

    return jsonify(user_schema.dump(user)), 200

# Route DELETE pour supprimer un utilisateur (ADMIN uniquement)
@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="Utilisateur non trouvé")
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200

# ----------------- ROUTES POUR AUTHENTIFICATION -----------------

# Route POST pour la connexion utilisateur et génération de token
@api_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Vérifier si les champs 'email' et 'password' sont présents
        if not data or not 'email' in data or not 'password' in data:
            return jsonify({'message': 'Données manquantes'}), 400

        # Rechercher l'utilisateur dans la base de données
        user = User.query.filter_by(email=data['email']).first()

        # Vérifier le mot de passe
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'message': 'Login ou mot de passe incorrect'}), 401

        # Générer le token JWT pour l'utilisateur
        access_token = generate_token(user)

        return jsonify({'token': access_token}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ----------------- ROUTES ITEMS -----------------

# Route POST pour créer un nouvel item (Utilisateur connecté uniquement)
@api_bp.route('/items', methods=['POST'])
@token_required
def create_item():
    data = request.get_json()

    current_user = request.current_user

    if not data or not 'name' in data:
        abort(400, description="Données manquantes")

    # Création d'un nouvel item
    new_item = Item(
        name=data['name'],
        description=data.get('description', ''),
        user_id=current_user.id  # L'utilisateur connecté est associé à l'item
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify(item_schema.dump(new_item)), 201

# Route GET pour récupérer tous les items (ADMIN uniquement)
@api_bp.route('/items', methods=['GET'])
@token_required
@role_required('admin')
def get_items():
    items = Item.query.all()
    if not items:
        abort(404, description="Aucun item trouvé")
    return jsonify(items_schema.dump(items)), 200

# Route GET pour récupérer un item spécifique (Propriétaire de l'item ou ADMIN)
@api_bp.route('/items/<int:item_id>', methods=['GET'])
@token_required
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, description="Item non trouvé")

    current_user = request.current_user
    if current_user.id != item.user_id and current_user.role != 'admin':
        abort(403, description="Accès refusé")

    return jsonify(item_schema.dump(item)), 200

# Route PUT pour mettre à jour un item (Propriétaire de l'item ou ADMIN)
@api_bp.route('/items/<int:item_id>', methods=['PUT'])
@token_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    current_user = request.current_user

    if current_user.id != item.user_id and current_user.role != 'admin':
        abort(403, description="Accès refusé")

    data = request.get_json()

    if not data:
        abort(400, description="Aucune donnée fournie")

    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)

    db.session.commit()

    return jsonify(item_schema.dump(item)), 200

# Route DELETE pour supprimer un item (Propriétaire de l'item ou ADMIN)
@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    current_user = request.current_user

    if current_user.id != item.user_id and current_user.role != 'admin':
        abort(403, description="Accès refusé")

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item supprimé avec succès'}), 200
