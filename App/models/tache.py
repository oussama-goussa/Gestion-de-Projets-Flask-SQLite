# models/tache.py

from .db import db

class Tache(db.Model):
    __tablename__ = 'tache'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    statut = db.Column(db.String(20), nullable=False)

    # Clés étrangères
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id', name='fk_tache_utilisateur_id', ondelete='CASCADE'), nullable=False)
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id', name='fk_tache_projet_id', ondelete='CASCADE'), nullable=False)

    # Relations explicites
    utilisateur = db.relationship('Utilisateur', back_populates='taches')
    projet = db.relationship('Projet', back_populates='taches')

    def __repr__(self):
        return f'Tache({self.titre}, {self.statut})'
