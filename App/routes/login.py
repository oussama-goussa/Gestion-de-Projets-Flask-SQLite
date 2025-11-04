# routes/login.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.auth import authenticate_user

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Le nom d'utilisateur et le mot de passe sont requis", 'danger')
            # Redirect to login page using blueprint's prefix (routes.login)
            return render_template('login.html')  # Corrected: use routes.login instead of login

        # Authenticate the user using the helper function
        user = authenticate_user(username, password)
        if not user:
            flash("Nom d'utilisateur ou mot de passe invalide", 'danger')
            # Redirect to login page using blueprint's prefix (routes.login)
            return render_template('login.html')

        # Set session variables after successful login
        session['user_id'] = user.id
        session['username'] = user.username
        # Redirect to home page using blueprint's prefix
        return redirect(url_for('home.index'))  # Corrected: use routes.home instead of home

    return render_template('login.html', show_nav=False)
