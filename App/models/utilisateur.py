# models/utilisateur.py

from .db import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relation explicite avec Tache
    taches = db.relationship('Tache', cascade='all, delete-orphan', back_populates='utilisateur')

    # Relation explicite avec Projet via la table d'association
    projets = db.relationship('Projet', secondary='projet_utilisateur', back_populates='utilisateurs')

    def __repr__(self):
        return f'Utilisateur({self.nom}, {self.email})'