from flask_sqlalchemy import SQLAlchemy
from flask_login     import LoginManager , UserMixin
from datetime            import datetime
db             = SQLAlchemy()
login_manager  = LoginManager()

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(67), unique=True, nullable=False)
    email    = db.Column(db.String(67), unique=True, nullable=False)
    password = db.Column(db.String(67), nullable=False)


API_KEY = "erm idk"

