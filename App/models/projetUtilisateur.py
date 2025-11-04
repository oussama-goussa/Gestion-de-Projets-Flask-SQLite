# models/projet_utilisateur.py

from .db import db

class ProjetUtilisateur(db.Model):
    __tablename__ = 'projet_utilisateur'
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id', name='fk_projet_utilisateur_id', ondelete='CASCADE'), primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id', name='fk_utilisateur_projet_id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f'ProjetUtilisateur(projet_id={self.projet_id}, utilisateur_id={self.utilisateur_id})'
