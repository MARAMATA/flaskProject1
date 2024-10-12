# Projet Flask API RESTful

## Description
Ce projet est une API RESTful développée avec Flask, sans utiliser Flask-RESTful. Elle implémente des fonctionnalités de base comme la gestion des utilisateurs et des items, ainsi que des fonctionnalités avancées comme la sérialisation des données et l'authentification avec JWT.

## Structure du projet
Voici une explication de chaque fichier et dossier dans la structure du projet :

- **app/__init__.py** : Ce fichier initialise l’application Flask et configure les extensions (SQLAlchemy, Marshmallow, etc.).
- **app/models.py** : Contient les modèles de base de données définis avec SQLAlchemy.
- **app/routes.py** : Contient les routes de l'API qui géreront les requêtes HTTP (GET, POST, PUT, DELETE).
- **app/schemas.py** : Gère la sérialisation et la désérialisation des données avec Marshmallow.
- **app/auth.py** : S'occupe des fonctionnalités d'authentification et d’autorisation.
- **app/utils.py** : Contiendra des fonctions utilitaires, comme la configuration de Swagger pour la documentation.
- **migrations/** : Dossier où Flask-Migrate stockera les fichiers de migration de base de données.
- **tests/** : Contiendra les tests unitaires pour valider les fonctionnalités de l'API.
- **.flaskenv** : Fichier contenant les variables d'environnement nécessaires au fonctionnement de Flask.
- **config.py** : Contiendra les configurations pour Flask (développement, production, etc.).
- **run.py** : Point d’entrée de l’application Flask, c'est ici que nous lancerons l'application.

## Explication des types de colonnes et des contraintes de base
db.Integer : Type entier, utilisé pour des colonnes comme les identifiants (ID).
db.String : Type chaîne de caractères, avec une limite de caractères.
primary_key=True : Définit la colonne comme clé primaire de la table.
nullable=False : Empêche que cette colonne accepte des valeurs nulles.
unique=True : Garantit que la valeur dans cette colonne est unique dans la table.
Ajout de relations entre les modèles
Relation One-to-Many : Dans l'exemple ci-dessus, un utilisateur peut avoir plusieurs items, mais chaque item appartient à un seul utilisateur.
Dans le modèle User, la relation est définie avec db.relationship('Item', backref='owner', lazy=True).
Dans le modèle Item, une clé étrangère user_id fait référence à la table users avec db.ForeignKey('users.id').

## Explication des champs et des validations :
fields.Int : Champ pour les entiers. Le paramètre dump_only=True signifie que ce champ sera uniquement utilisé pour la sérialisation (pas pour la désérialisation).
fields.Str : Champ pour les chaînes de caractères. Le paramètre required=True signifie que ce champ est obligatoire.
fields.Email : Champ pour les adresses e-mail, avec validation automatique pour s'assurer que l'adresse est valide.
fields.Nested : Utilisé pour inclure un schéma imbriqué, ici pour lister les items appartenant à un utilisateur dans le schéma UserSchema.
load_only=True : Indique que le champ est utilisé uniquement pour la désérialisation, typiquement pour des informations sensibles comme le mot de passe.
validate.Length(min=3) : Validation pour s'assurer que la chaîne de caractères a au moins trois caractères.


## Explication de chaque méthode HTTP :
GET : Récupère une ou plusieurs ressources.

get_users() : Récupère tous les utilisateurs.
get_user(user_id) : Récupère un utilisateur spécifique avec son ID.
POST : Crée une nouvelle ressource.

create_user() : Crée un nouvel utilisateur après avoir validé les données fournies par le client.
PUT : Met à jour une ressource existante.

update_user(user_id) : Met à jour un utilisateur spécifique avec les nouvelles données.
DELETE : Supprime une ressource.

delete_user(user_id) : Supprime un utilisateur avec son ID.
2.Gestion des erreurs et réponses
Pour gérer les erreurs dans Flask, il est essentiel de retourner des réponses appropriées avec des statuts HTTP corrects.

Exemple de gestion d’erreurs :
404 (Not Found) : Utilisation de get_or_404 qui renvoie automatiquement une erreur 404 si l’ID n’est pas trouvé.
400 (Bad Request) : Si les données sont manquantes ou invalides, un statut 400 est renvoyé avec un message d'erreur explicatif.

- Structurer les réponses JSON :
Pour garantir la cohérence des réponses :

Réponses réussies : Retourner les données sérialisées en JSON avec un statut HTTP 200 (ou 201 pour les créations).
Réponses en cas d’erreur : Retourner un message d'erreur structuré en JSON avec le statut approprié (400, 404, etc.).

- Utilisation des Blueprints pour organiser les routes
Les Blueprints dans Flask permettent de regrouper les routes liées à une fonctionnalité spécifique (comme users ou items) dans des modules séparés, rendant le projet plus organisé et modulaire.

## Partie 5: Documentation de l’API
1. Documentation avec Swagger
Importance de documenter une API
La documentation d'une API est cruciale car elle permet aux développeurs de comprendre comment interagir avec les différents endpoints de l'API. Une bonne documentation inclut des informations sur :

Les endpoints disponibles.
Les méthodes HTTP acceptées (GET, POST, PUT, DELETE).
Les paramètres requis et les formats de réponse.
Les erreurs potentielles et comment les traiter.
Cela facilite l'intégration et l'utilisation de l'API par d'autres développeurs et équipes. Une documentation interactive, comme celle fournie par Swagger, permet de tester directement les requêtes depuis le navigateur.

2.Utilisation de Swagger pour documenter votre API
Swagger est un outil puissant qui permet de générer automatiquement une documentation interactive pour les APIs RESTful. Il fournit une interface visuelle qui décrit les endpoints de l’API, les méthodes HTTP disponibles, et les exemples de requêtes et de réponses.


## Documentation de l'API avec Swagger

Vous pouvez accéder à la documentation de l'API générée avec Swagger en cliquant sur le lien ci-dessous :

[Consulter la documentation Swagger](http://127.0.0.1:5000/swagger/)

### Importance de Swagger
La documentation d'une API est cruciale pour faciliter l'intégration et l'utilisation par d'autres développeurs. Swagger permet de visualiser et de tester directement les endpoints de l'API.

### Utilisation de Swagger
- Pour accéder à la documentation de l'API, suivez ce lien : [Documentation Swagger](http://127.0.0.1:5000/swagger/).
- Vous pouvez tester chaque endpoint et voir les réponses directement depuis cette interface.


## Partie 6: Authentification et Autorisation
1. Implémentation de l’authentification
Concepts d’authentification et d’autorisation : L'authentification est le processus de vérification de l'identité d'un utilisateur. Cela implique souvent de valider des informations d'identification telles que le nom d'utilisateur et le mot de passe. L'autorisation, quant à elle, détermine si un utilisateur authentifié a le droit d'accéder à certaines ressources ou fonctionnalités dans une application.

Utilisation des jetons JWT : Les jetons JWT (JSON Web Tokens) sont utilisés pour sécuriser les endpoints de l'API. Lorsqu'un utilisateur se connecte avec succès, un jeton JWT est généré et renvoyé au client. Ce jeton doit être inclus dans l'en-tête des requêtes pour accéder à des routes protégées.

### Exemples d’implémentation de routes :

#### Route de connexion: 
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({'message': 'Données manquantes'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Login ou mot de passe incorrect'}), 401

    access_token = generate_token(user)
    return jsonify({'access_token': access_token}), 200

#### Protection des routes avec des jetons d’authentification :

@api_bp.route('/users', methods=['GET'])
@token_required
def get_users():
    users = User.query.all()
    if not users:
        abort(404, description="Aucun utilisateur trouvé")
    return jsonify(users_schema.dump(users)), 200


2. Gestion des rôles et permissions
Implémentation d’un système de rôles : Le système de rôles permet de définir différents types d'utilisateurs 
(par exemple, admin et user) avec des permissions spécifiques. Cela se fait par l'attribut role dans le modèle User.

#### Lors de la création d'un nouvel utilisateur, vous pouvez spécifier le rôle :

new_user = User(
    username=data['username'],
    email=data['email'],
    password_hash=hashed_password,
    role=data['role']  # Utilisation du rôle fourni dans les données
)


#### Restriction de l’accès aux routes :

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

Les routes protégées, comme la suppression d'un utilisateur, utilisent le décorateur @role_required('admin') 
pour s'assurer que seul un utilisateur avec le rôle d'administrateur peut accéder à ces fonctionnalités 


## Partie 7: Tests et Déploiement
1. Écriture de tests unitaires
Importance des tests unitaires pour garantir la fiabilité de l’API
Les tests unitaires sont cruciaux pour assurer la fiabilité et la robustesse d'une API. Ils permettent de vérifier que chaque composant de l'application fonctionne comme prévu, en testant des fonctions, des méthodes et des routes spécifiques de manière isolée. Voici quelques raisons pour lesquelles les tests unitaires sont importants :

Détection précoce des erreurs : En exécutant régulièrement des tests unitaires, les développeurs peuvent identifier et corriger les bogues avant qu'ils ne deviennent des problèmes majeurs en production.
Documentation vivante : Les tests servent de documentation pour le comportement attendu de l'API, ce qui facilite la compréhension pour les nouveaux développeurs ou les parties prenantes.
Régression : Les tests unitaires permettent de s'assurer que les modifications apportées à une partie du code n'introduisent pas de nouveaux bogues dans d'autres parties de l'application.
Confiance lors des refactorisations : Lorsque des modifications majeures sont nécessaires, les tests unitaires offrent une certaine tranquillité d'esprit, car les développeurs peuvent exécuter les tests pour s'assurer que tout fonctionne toujours.


## Utilisation de bibliothèques comme unittest ou pytest
Dans le code test_app.py, nous utilisons la bibliothèque pytest pour écrire et exécuter nos tests. Voici comment cela fonctionne :

1. Installation de pytest : 

pip install pytest


2. Structure du code de test :

import pytest
import json
from app import create_app, db
from app.models import User, Item
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.from_object('test_config.TestConfig')

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database():
    user = User(username='testuser', email='testuser@example.com', password_hash=generate_password_hash('password123'))
    db.session.add(user)
    db.session.commit()

    yield db
    db.session.remove()
    db.drop_all()

# Test pour les utilisateurs
def test_create_user(client):
    new_user = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    }
    response = client.post('/api/users', data=json.dumps(new_user), content_type='application/json')
    assert response.status_code == 201

# Test pour les items
def test_create_item(client, init_database):
    new_item = {
        'name': 'item1',
        'description': 'A test item',
        'user_id': 1
    }
    response = client.post('/api/items', data=json.dumps(new_item), content_type='application/json')
    assert response.status_code == 201


3. Exécution des tests :

pytest test_app.py



2. Déploiement de l’API :

Voici un guide étape par étape pour créer un environnement Elastic Beanstalk et déployer mon application Flask en utilisant la ligne de commande (CLI) :

Étape 1 : Installer les Outils nécessaires
Je dois m'assurer d'avoir les outils suivants installés sur ma machine :

AWS CLI : Pour l'installer, je peux suivre les instructions officielles disponibles sur le site d'AWS.
EB CLI (Elastic Beanstalk Command Line Interface) : Je peux l'installer avec la commande suivante :

pip install awsebcli

Étape 2 : Configurer AWS CLI
Avant de créer un environnement Elastic Beanstalk, je dois configurer AWS CLI avec mes informations d'identification :


aws configure

Je serai invité à entrer :

Ma clé d'accès AWS
Ma clé secrète AWS
Ma région par défaut (par exemple, us-west-2)
Mon format de sortie par défaut (je peux laisser cela vide)

Étape 3 : Initialiser mon Application

Je me rends dans le répertoire de mon projet Flask et j'exécute la commande suivante pour initialiser mon application Elastic Beanstalk :

eb init -p python-3.x nom_de_mon_application
Je remplace nom_de_mon_application par le nom que je souhaite pour mon application. Il est important de choisir la version Python appropriée (ici, python-3.12).

Étape 4 : Créer un Environnement Elastic Beanstalk
Une fois mon application initialisée, je peux créer un nouvel environnement avec la commande suivante :

eb create nom_de_mon_environnement

Je remplace nom_de_mon_environnement par un nom pour l'environnement (par exemple, production ou dev). Cela créera un environnement Elastic Beanstalk et déploiera mon application.

Étape 5 : Déployer mon Application
Si j'ai effectué des modifications dans mon code et que je souhaite déployer à nouveau mon application, j'utilise cette commande :

eb deploy

Étape 6 : Vérifier l'État de l'Environnement
Je peux vérifier l'état de mon environnement en exécutant cette commande :

eb status

Étape 7 : Accéder à mon Application
Une fois le déploiement terminé, je peux accéder à mon application via l'URL fournie par Elastic Beanstalk. Je peux aussi ouvrir l'application dans mon navigateur avec la commande suivante :

eb open

Étape 8 : Configurer les Variables d'Environnement
Pour configurer les variables d'environnement nécessaires à mon application, j'utilise la commande suivante :


eb setenv SECRET_KEY=ma_secret_key DATABASE_URL=mon_database_url

Je remplace ma_secret_key et mon_database_url par les valeurs appropriées.

Étape 9 : Conteneuriser mon Application avec Docker 
Si je souhaite utiliser Docker pour conteneuriser mon application Flask avant de la déployer, je dois ajouter un fichier Dockerfile à la racine de mon projet. Voici un exemple de Dockerfile :

# Utiliser l'image Python comme base
FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# Exposer le port 5000
EXPOSE 5000

# Lancer l'application
CMD ["flask", "run", "--host=0.0.0.0"]
Ensuite, lors de l'initialisation de l'application, je spécifie que j'utilise Docker avec cette commande :

eb init -p docker nom_de_mon_application

Après avoir créé mon Dockerfile, je peux déployer mon application avec eb create ou eb deploy comme précédemment décrit.




## Installation et configuration

1. Cloner le projet
   ```bash
   git clone <url-du-repository>
   cd flask_api_project
