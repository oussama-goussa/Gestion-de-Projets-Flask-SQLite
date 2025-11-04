# routes/utilisateurs.py

from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from models.utilisateur import Utilisateur
from models.db import db

utilisateurs_bp = Blueprint('utilisateurs', __name__)

@utilisateurs_bp.route('/', methods=['GET'])
def lister_utilisateurs():
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    utilisateurs = Utilisateur.query.all()  # Récupérer tous les utilisateurs
    return render_template('utilisateurs.html', utilisateurs = utilisateurs, show_nav=True)

@utilisateurs_bp.route('/ajouter', methods=['GET', 'POST'])
def ajouter_utilisateur():
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    if request.method == 'POST':
        nom = request.form['nom']  # Get the data from the form
        email = request.form['email']
        
        # Check if the email already exists
        utilisateur_exist = Utilisateur.query.filter_by(email=email).first()
        if utilisateur_exist:
            return render_template('utilisateurs.html', error="Utilisateur avec cet email existe déjà", utilisateurs=Utilisateur.query.all(), show_nav=True)
        
        # Add the new utilisateur
        utilisateur = Utilisateur(nom=nom, email=email)
        db.session.add(utilisateur)
        db.session.commit()

        # Rediriger vers la liste des utilisateurs après ajout
        # return redirect(url_for('utilisateurs.lister_utilisateurs'))
        return render_template('utilisateurs.html', success="L'utilisateur ajouté avec succès", utilisateurs=Utilisateur.query.all(), show_nav=True)

    return render_template('utilisateurs.html', show_nav=True)  # Render a form page to add a new user

@utilisateurs_bp.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_utilisateur(id):
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    utilisateur = Utilisateur.query.get(id)  # Récupérer l'utilisateur par son ID
    
    if request.method == 'POST':
        utilisateur.nom = request.form['nom']
        utilisateur.email = request.form['email']
        
        # Mettre à jour l'utilisateur dans la base de données
        db.session.commit()
        return render_template('utilisateurs.html', success="L'utilisateur mise à jour avec succès", utilisateurs=Utilisateur.query.all(), show_nav=True)

        return redirect(url_for('utilisateurs.lister_utilisateurs'))  # Rediriger vers la liste des utilisateurs

    # Si la méthode est GET, afficher le formulaire avec les informations de l'utilisateur
    return render_template('modifier_utilisateur.html', utilisateur=utilisateur)

@utilisateurs_bp.route('/supprimer/<int:id>', methods=['GET'])
def supprimer_utilisateur(id):
    if 'user_id' not in session:
        flash('You must log in to access this page.', 'danger')
        return redirect(url_for('login.login'))
    
    utilisateur = Utilisateur.query.get(id)  # Récupérer l'utilisateur par son ID
    
    if utilisateur:
        db.session.delete(utilisateur)  # Supprimer l'utilisateur de la base de données
        db.session.commit()
    
    # return redirect(url_for('utilisateurs.lister_utilisateurs'))  # Rediriger vers la liste des utilisateurs
    return render_template('utilisateurs.html', success="L'utilisateur supprimé avec succès", utilisateurs=Utilisateur.query.all(), show_nav=True)


