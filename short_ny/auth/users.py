from flask import Blueprint, flash, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from ..models import User
from ..extensions import db


auth = Blueprint('auth', __name__)



@auth.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shortner.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('This username already exists.')
            return redirect(url_for('auth.register'))

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('This email is already registered.')
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)

        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('You are now signed up.')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shortner.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash('You are now logged in.')
                return redirect(url_for('shortner.index'))
            
            if (user and check_password_hash(user.password_hash, password)) == False:
                flash('Please provide valid credentials.')
                return redirect(url_for('auth.login'))

        else:
            flash('Account not found. Please sign up to continue.')
            return redirect(url_for('auth.register'))
        
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('shortner.index'))




