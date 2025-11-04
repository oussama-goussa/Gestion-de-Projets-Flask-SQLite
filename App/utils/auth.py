from flask_bcrypt import Bcrypt
from models.db import db
from models.user import User

bcrypt = Bcrypt()

def create_user(username, email, password):
    """Create a new user in the database."""
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

def authenticate_user(username, password):
    """Authenticate a user by username and password."""
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None