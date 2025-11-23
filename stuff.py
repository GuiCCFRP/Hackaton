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


API_KEY = "sk-hc-v1-a116620997e2443a9f23bef82a50ec014fe9d189a8dc46339bc6f3415bb8c515" #YES TS IS RAGEBAIT :)))))))))
