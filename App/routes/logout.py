# routes/logout.py

from flask import Blueprint, redirect, url_for, flash, session
from utils.auth import authenticate_user

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Supprimer les variables de session
    session.pop('username', None)
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('login.login'))  # Rediriger vers la page de login