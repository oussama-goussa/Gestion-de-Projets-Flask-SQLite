from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.auth import create_user
from models.user import User

register_bp = Blueprint('register', __name__)

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate inputs
        if not username or not email or not password or not confirm_password:
            flash('Tous les champs sont obligatoires', 'danger')
            return redirect(url_for('register.register'))

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'danger')
            return redirect(url_for('register.register'))

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash("Nom d'utilisateur déjà existant", 'danger')
            return redirect(url_for('register.register'))

        if User.query.filter_by(email=email).first():
            flash('Adresse e-mail déjà existant', 'danger')
            return redirect(url_for('register.register'))

        # Create the user
        create_user(username, email, password)
        flash('Utilisateur enregistré avec succès!', 'success')
        return redirect(url_for('login.login'))

    return render_template('register.html', show_nav=False)