class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gestion_projet.db'  # Exemple avec SQLite
    SECRET_KEY = 'votre_clé_secrète'
    JSON_FILE_PATH = "gestion_projets.json"