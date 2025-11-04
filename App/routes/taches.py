# routes/projet_utilisateur.py

from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from models.tache import Tache
from models.projet import Projet
from models.utilisateur import Utilisateur
from models.db import db
from models.projet import Projet
from models.projetUtilisateur import ProjetUtilisateur
from flask import Blueprint, jsonify, request

taches_bp = Blueprint('taches', __name__)

# Lister les tâches
# @taches_bp.route('/', methods=['GET'])
# def lister_taches():
#    taches = Tache.query.all()
#    return render_template('taches.html', taches=taches, utilisateurs=Utilisateur.query.all(), projets=Projet.query.all())

@taches_bp.route('/', methods=['GET'])
def lister_taches():
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    taches = Tache.query.all()
    return render_template('taches.html', taches=taches, utilisateurs=Utilisateur.query.all(), projets=Projet.query.all(), show_nav=True)

# Ajouter une tâche (via formulaire HTML)
@taches_bp.route('/ajouter', methods=['GET', 'POST'])
def ajouter_tache():
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        statut = request.form['statut']
        utilisateur_id = request.form['utilisateur_id']
        projet_id = request.form['projet_id']
        
        # Récupérer l'utilisateur et le projet par leurs ID
        utilisateur = Utilisateur.query.get(utilisateur_id)
        projet = Projet.query.get(projet_id)
        
        if not utilisateur or not projet:
            return render_template('taches.html', error="Utilisateur ou projet non trouvé", taches = Tache.query.all(), utilisateurs=Utilisateur.query.all(), projets=Projet.query.all(), show_nav=True)
        
        # Ajouter la tâche
        nouvelle_tache = Tache(titre=titre, description=description, statut=statut, utilisateur_id=utilisateur.id, projet_id=projet.id)
        db.session.add(nouvelle_tache)
        db.session.commit()
        
        # return redirect(url_for('taches.lister_taches'))  # Rediriger vers la liste des tâches
        # Message de succès et redirection vers la page des projets
        return render_template('taches.html', success="La tâche ajouté avec succès", taches = Tache.query.all(), utilisateurs=Utilisateur.query.all(), projets=Projet.query.all(), show_nav=True)

    
    # Si la méthode est GET, afficher le formulaire pour ajouter une tâche
    return render_template('taches.html', utilisateurs=Utilisateur.query.all(), projets=Projet.query.all(), show_nav=True)  # Récupérer les utilisateurs et projets

# Modifier une tâche
@taches_bp.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_tache(id):
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    tache = Tache.query.get(id)  # Récupérer la tâche par son ID
    utilisateurs = Utilisateur.query.all()  # Liste des utilisateurs
    projets = Projet.query.all()  # Liste des projets

    if request.method == 'POST':
        tache.titre = request.form['titre']
        tache.description = request.form['description']
        tache.statut = request.form['statut']
        tache.utilisateur_id = request.form['utilisateur_id']
        tache.projet_id = request.form['projet_id']

        # Mettre à jour la tâche dans la base de données
        db.session.commit()
        return render_template('taches.html', success="La tâche mise à jour avec succès", taches = Tache.query.all(), utilisateurs=utilisateurs, projets=projets, show_nav=True)

    # Si la méthode est GET, afficher le formulaire avec les informations de la tâche
    return render_template('modifier_tache.html', tache=tache, utilisateurs=utilisateurs, projets=projets)

# Supprimer une tâche
@taches_bp.route('/supprimer/<int:id>', methods=['GET'])
def supprimer_tache(id):
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    tache = Tache.query.get(id)  # Récupérer la tâche par son ID
    
    if tache:
        db.session.delete(tache)  # Supprimer la tâche de la base de données
        db.session.commit()
    
    return render_template('taches.html', success="La tâche supprimé avec succès",taches = Tache.query.all(), projets=Projet.query.all(), utilisateurs=Utilisateur.query.all(), show_nav=True)
    # return redirect(url_for('taches.lister_taches'))  # Rediriger vers la liste des tâches

@taches_bp.route('/projets/<int:utilisateur_id>', methods=['GET'])
def get_projets_par_utilisateur(utilisateur_id):
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    # Récupérer les projets associés à l'utilisateur
    projets = db.session.query(Projet).join(ProjetUtilisateur).filter(ProjetUtilisateur.utilisateur_id == utilisateur_id).all()
    
    # Convertir les projets en format JSON
    projets_data = [{"id": projet.id, "nom": projet.nom} for projet in projets]
    
    return {"projets": projets_data}


