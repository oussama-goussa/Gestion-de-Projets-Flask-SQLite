# routes/home.py

from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask import jsonify
from models.projet import Projet
from models.utilisateur import Utilisateur
from models.db import db
from flask import current_app
from models.tache import Tache
import json

# Créer un blueprint pour la route principale
home_bp = Blueprint('home', __name__)

# Vérification si l'utilisateur est authentifié
def is_authenticated():
    return 'user_id' in session

# Décorateur pour protéger la route
def login_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login.login'))  # Rediriger vers la page de login si non authentifié
        return f(*args, **kwargs)

    return decorated_function

# Définir la route principale
@home_bp.route('/')
@login_required
def index():
    # Calcul des statistiques
    stats = {
        'a_faire': Tache.query.filter_by(statut='À faire').count(),
        'en_cours': Tache.query.filter_by(statut='En cours').count(),
        'termine': Tache.query.filter_by(statut='Terminé').count(),
    }

    return render_template('index.html', username=session.get('username'), show_nav=True, stats=stats)

# Sauvegarder les projets et utilisateurs dans un fichier JSON
@home_bp.route('/sauvegarder', methods=['POST'])
def sauvegarder():
    try:
        # Récupérer les données
        projets = Projet.query.all()
        utilisateurs = Utilisateur.query.all()

        # Préparer les données à sauvegarder
        data = {
            "projets": [
                {
                    "nom": projet.nom,
                    "description": projet.description,
                    "taches": [
                        {
                            "titre": tache.titre,
                            "description": tache.description,
                            "statut": tache.statut,
                            "utilisateur": {
                                "nom": tache.utilisateur.nom,
                                "email": tache.utilisateur.email,
                            },
                        }
                        for tache in projet.taches
                    ],
                    "utilisateurs": [
                        {
                            "nom": utilisateur.nom,
                            "email": utilisateur.email,
                        }
                        for utilisateur in projet.utilisateurs  # Liste de tous les utilisateurs associés
                    ],
                }
                for projet in projets
            ],
            "utilisateurs": [
                {"nom": utilisateur.nom, "email": utilisateur.email}
                for utilisateur in utilisateurs
            ],
        }

        # Sauvegarder dans un fichier JSON
        with open("gestion_projets.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        flash("Données sauvegardées avec succès !", "success")
    except Exception as e:
        flash(f"Erreur lors de la sauvegarde : {str(e)}", "danger")

    return redirect(url_for('home.index'))

from sqlalchemy import text

# Charger les projets et utilisateurs depuis un fichier JSON
@home_bp.route('/charger', methods=['POST'])
def charger():
    try:
        # Charger les données depuis le fichier JSON
        with open("gestion_projets.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Effacer les données existantes
        Tache.query.delete()
        Projet.query.delete()
        Utilisateur.query.delete()
        db.session.execute(text('DELETE FROM projet_utilisateur'))  # Effacer les associations existantes
        db.session.commit()

        # Réinsérer les utilisateurs
        utilisateurs = {}
        for utilisateur_data in data["utilisateurs"]:
            utilisateur = Utilisateur(
                nom=utilisateur_data["nom"], email=utilisateur_data["email"]
            )
            db.session.add(utilisateur)
            utilisateurs[utilisateur_data["email"]] = utilisateur

        # Réinsérer les projets
        for projet_data in data["projets"]:
            projet = Projet(
                nom=projet_data["nom"], description=projet_data["description"]
            )
            db.session.add(projet)

            # Ajouter les tâches
            for tache_data in projet_data["taches"]:
                utilisateur = utilisateurs.get(tache_data["utilisateur"]["email"])
                if utilisateur:
                    tache = Tache(
                        titre=tache_data["titre"],
                        description=tache_data["description"],
                        statut=tache_data["statut"],
                        utilisateur=utilisateur,
                        projet=projet,
                    )
                    db.session.add(tache)

            # Ajouter les utilisateurs au projet (many-to-many relationship)
            for utilisateur_data in projet_data["utilisateurs"]:
                utilisateur = utilisateurs.get(utilisateur_data["email"])
                if utilisateur:
                    projet.utilisateurs.append(utilisateur)

        db.session.commit()
        flash("Données chargées avec succès !", "success")
    except Exception as e:
        flash(f"Erreur lors du chargement : {str(e)}", "danger")

    return redirect(url_for('home.index'))