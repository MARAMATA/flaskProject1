from functools import wraps
from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from .models import User
from werkzeug.security import check_password_hash

# Fonction pour générer un token JWT
def generate_token(user):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)  # Expire en 1 heure
    return s.dumps({'user_id': user.id}).decode('utf-8')

# Route de connexion
def login():
    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({'message': 'Données manquantes'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Login ou mot de passe incorrect !'}), 401

    access_token = generate_token(user)
    return jsonify({'access_token': access_token}), 200

# Fonction pour vérifier le jeton JWT
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Jeton manquant !'}), 403

        try:
            s = Serializer(current_app.config['SECRET_KEY'])
            data = s.loads(token)
        except SignatureExpired:
            return jsonify({'message': 'Jeton expiré !'}), 403
        except BadSignature:
            return jsonify({'message': 'Jeton invalide !'}), 403

        return f(*args, **kwargs)

    return decorated_function

# Vérification du rôle pour accéder à certaines routes
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Jeton manquant !'}), 403

            try:
                s = Serializer(current_app.config['SECRET_KEY'])
                data = s.loads(token)
            except:
                return jsonify({'message': 'Jeton invalide !'}), 403

            user_id = data['user_id']
            user = User.query.get(user_id)

            if not user or user.role != role:
                return jsonify({'message': f'Accès interdit, rôle {role} requis'}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


