from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Instances des extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

# Configuration de Swagger
SWAGGER_URL = '/swagger'  # URL pour accéder à Swagger UI
API_URL = '/swaggerfile'  # URL du fichier swagger.json

# Configurer Swagger
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI endpoint
    API_URL,      # URL du swagger.json
    config={       # Swagger UI configuration
        'app_name': "Flask API"
    }
)

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    # Activer CORS pour toute l'application
    CORS(app)

    # Route pour servir manuellement swagger.json
    @app.route('/swaggerfile')
    def serve_swagger():
        return send_from_directory('static', 'swagger.json')

    # Charger la configuration de l'application
    app.config.from_object('config.Config')

    # Initialiser les extensions avec l'application
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Enregistrer les routes de l'API
    from .routes import api_bp
    app.register_blueprint(api_bp)

    # Enregistrement de Swagger UI
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
