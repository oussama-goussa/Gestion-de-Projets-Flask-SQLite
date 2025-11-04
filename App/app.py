from flask import Flask, session, redirect, url_for
from flask_migrate import Migrate
from routes.projets import projets_bp
from routes.utilisateurs import utilisateurs_bp
from routes.taches import taches_bp
from routes.login import login_bp
from routes.register import register_bp
from routes.logout import logout_bp
from routes.home import home_bp  # Importer le blueprint home
from config import Config
from models.db import db

# Importer les modèles après avoir importé db
from models.projet import Projet
from models.utilisateur import Utilisateur
from models.tache import Tache

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialiser la base de données
    db.init_app(app)

    # Initialiser Flask-Migrate
    migrate = Migrate(app, db)

    # Enregistrement des blueprints
    app.register_blueprint(projets_bp, url_prefix='/projets')
    app.register_blueprint(utilisateurs_bp, url_prefix='/utilisateurs')
    app.register_blueprint(taches_bp, url_prefix='/taches')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(logout_bp, url_prefix='/logout')
    app.register_blueprint(home_bp)  # Enregistrer le blueprint home sans préfixe

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
