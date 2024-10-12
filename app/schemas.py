from marshmallow import Schema, fields, validate

# Schéma de l'utilisateur
class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # Ce champ sera retourné uniquement dans les réponses
    username = fields.Str(required=True, validate=validate.Length(min=1))  # Le nom d'utilisateur est requis et doit avoir au moins 1 caractère
    email = fields.Email(required=True)  # L'email est requis et doit être une adresse email valide
    password = fields.Str(load_only=True, required=True)  # Le mot de passe est requis mais ne sera pas renvoyé dans les réponses

# Schéma des items
class ItemSchema(Schema):
    id = fields.Int(dump_only=True)  # Ce champ sera retourné uniquement dans les réponses
    name = fields.Str(required=True, validate=validate.Length(min=1))  # Le nom de l'item est requis
    description = fields.Str()  # La description est facultative
    user_id = fields.Int(required=True)  # Chaque item doit être lié à un utilisateur via user_id



