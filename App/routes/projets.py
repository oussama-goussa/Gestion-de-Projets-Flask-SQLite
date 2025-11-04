from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.projet import Projet
from models.utilisateur import Utilisateur
from models.db import db

projets_bp = Blueprint('projets', __name__)

# Lister les projets
@projets_bp.route('/', methods=['GET'])
def lister_projets():
    # Check if the user is logged in (based on session)
    if not session.get('user_id'):
        flash('You must log in to access the home page.', 'danger')
        return redirect(url_for('login.login'))
    
    projets = Projet.query.all()
    return render_template('projets.html', projets=projets, utilisateurs=Utilisateur.query.all(), show_nav=True)

# Ajouter un projet (via un formulaire HTML)
@projets_bp.route('/ajouter', methods=['GET', 'POST'])
def ajouter_projet():
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        utilisateur_ids = request.form.getlist('utilisateur_ids')  # Récupère la liste des IDs des utilisateurs sélectionnés
        
        # Vérifier si un projet avec le même nom existe déjà
        projet_existant = Projet.query.filter_by(nom=nom).first()
        if projet_existant:
            # Renvoyer un message d'erreur si le projet existe déjà
            return render_template('projets.html', error="Un projet avec ce nom existe déjà", projets=Projet.query.all(), utilisateurs=Utilisateur.query.all(), show_nav=True)
        
        # Récupérer les utilisateurs par leurs IDs
        utilisateurs = Utilisateur.query.filter(Utilisateur.id.in_(utilisateur_ids)).all()
        
        # Ajouter le projet
        nouveau_projet = Projet(nom=nom, description=description)
        nouveau_projet.utilisateurs = utilisateurs  # Associer les utilisateurs au projet
        
        db.session.add(nouveau_projet)
        db.session.commit()
        
        # Message de succès et redirection vers la page des projets
        return render_template('projets.html', success="Projet ajouté avec succès", projets=Projet.query.all(), utilisateurs=Utilisateur.query.all(), show_nav=True)

    return render_template('projets.html', utilisateurs=Utilisateur.query.all(), show_nav=True)  # Formulaire pour ajouter un projet

# Modifier un projet
@projets_bp.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_projet(id):
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    projet = Projet.query.get(id)  # Récupérer le projet par son ID
    
    if request.method == 'POST':
        projet.nom = request.form['nom']
        projet.description = request.form['description']
        
        # Récupérer les utilisateurs sélectionnés
        utilisateur_ids = request.form.getlist('utilisateur_ids')
        utilisateurs = Utilisateur.query.filter(Utilisateur.id.in_(utilisateur_ids)).all()
        
        # Mettre à jour les utilisateurs associés au projet
        projet.utilisateurs = utilisateurs
        
        # Mettre à jour le projet dans la base de données
        db.session.commit()
        
        # Message de succès et redirection vers la page des projets
        # return redirect(url_for('projets.lister_projets', success="Projet mis à jour avec succès"))
        return render_template('projets.html', success="Projet mis à jour avec succès", projets=Projet.query.all(), utilisateurs=Utilisateur.query.all(), show_nav=True)

    # Si la méthode est GET, afficher le formulaire avec les informations du projet
    return render_template('modifier_projet.html', projet=projet, utilisateurs=Utilisateur.query.all())

# Supprimer un projet
@projets_bp.route('/supprimer/<int:id>', methods=['GET'])
def supprimer_projet(id):
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    projet = Projet.query.get(id)  # Récupérer le projet par son ID
    
    if projet:
        db.session.delete(projet)  # Supprimer le projet de la base de données
        db.session.commit()
    
    # Message de succès et redirection vers la liste des projets
    return render_template('projets.html', success="Projet supprimé avec succès", projets=Projet.query.all(), utilisateurs=Utilisateur.query.all(), show_nav=True)
    # return redirect(url_for('projets.lister_projets', success="Projet supprimé avec succès"))

