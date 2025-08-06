from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Outros campos serão adicionados posteriormente