from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from ..models.user import User
from .. import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        data = request.form
        
        if User.query.filter_by(email=data['email']).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(
            email=data['email'],
            name=data.get('name', ''),
            role='user'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', now=datetime.now())

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            login_user(user, remember=True)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            
            flash('Welcome back!', 'success')
            return redirect(next_page)
        
        flash('Invalid email or password', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html', now=datetime.now())

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html', now=datetime.now())

@bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return render_template('auth/profile.html', user=current_user, now=datetime.now())

@bp.route('/profile', methods=['POST'])
@login_required
def update_profile():
    data = request.form
    
    if 'name' in data:
        current_user.name = data['name']
    if 'password' in data and data['password']:
        current_user.set_password(data['password'])
    
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('auth.get_profile')) 