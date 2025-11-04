# models/projet.py

from .db import db

class Projet(db.Model):
    __tablename__ = 'projet'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Relation explicite avec Utilisateur via la table d'association
    utilisateurs = db.relationship('Utilisateur', secondary='projet_utilisateur', back_populates='projets')

    # Relation explicite avec Tache
    taches = db.relationship('Tache', cascade='all, delete-orphan', back_populates='projet')

    def __repr__(self):
        return f'Projet({self.nom}, {self.description})'
