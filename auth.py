# auth.py
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
)
from werkzeug.security import generate_password_hash, check_password_hash

from stuff import db, login_manager, User


auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET  -> render login page
    POST -> authenticate and redirect to main page
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')



@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Signup is expected to be submitted from login.html
    (no separate signup.html template).

    In login.html, the signup form should:
      action="{{ url_for('auth.signup') }}" method="POST"
    """
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not username or not email or not password:
        flash('All fields are required', 'danger')
        return redirect(url_for('auth.login'))


    if User.query.filter_by(username=username).first():
        flash('Username already in use', 'danger')
        return redirect(url_for('auth.login'))

    if User.query.filter_by(email=email).first():
        flash('Email already in use', 'danger')
        return redirect(url_for('auth.login'))

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('auth.login'))



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))



@auth_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('settings.html')



@auth_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    new_email = request.form.get('email', '').strip()
    new_username = request.form.get('username', '').strip()

    if not new_email:
        flash('Email cannot be empty', 'danger')
        return redirect(url_for('auth.settings'))

    if new_email == current_user.email and new_username == current_user.username:
        flash('No changes detected', 'info')
        return redirect(url_for('auth.settings'))

   
    if new_email != current_user.email:
        if User.query.filter_by(email=new_email).first():
            flash('Email already in use', 'danger')
            return redirect(url_for('auth.settings'))
        current_user.email = new_email

    
    if new_username and new_username != current_user.username:
        if User.query.filter_by(username=new_username).first():
            flash('Username already in use', 'danger')
            return redirect(url_for('auth.settings'))
        current_user.username = new_username

    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('auth.settings'))



@auth_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('Account deleted successfully', 'success')
    return redirect(url_for('auth.login'))



@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not check_password_hash(current_user.password, current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('auth.settings'))

    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('auth.settings'))

    if not new_password:
        flash('New password cannot be empty', 'danger')
        return redirect(url_for('auth.settings'))

    current_user.password = generate_password_hash(new_password)
    db.session.commit()
    flash('Password changed successfully', 'success')
    return redirect(url_for('auth.settings'))
