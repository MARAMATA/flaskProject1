from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Modèle User
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='user')

    # Relation One-to-Many (un utilisateur peut avoir plusieurs items)
    items = db.relationship('Item', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash the password before saving."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password matches the hash."""
        return check_password_hash(self.password_hash, password)

# Modèle Item
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'
