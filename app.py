# app.py
from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, current_user
from config import Config
from stuff import db, login_manager
import requests

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    
    with app.app_context():
        from stuff import User
        db.create_all()

   
    from auth import auth_bp
    from main_page import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)


    @app.route('/')
    def home():
        """
        Root URL.
        - If logged in -> show main page
        - If not logged in -> go to login view
        """
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return redirect(url_for('auth.login'))

    @app.route('/index')
    @login_required
    def index():
        """
        Main logged-in page (templates/index.html).
        """
        return render_template('index.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
