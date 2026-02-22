from flask import Blueprint, render_template, request, redirect, url_for, session, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('project.dashboard'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    auth_service = current_app.auth_service
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = auth_service.login(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('project.dashboard'))
        return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('project.dashboard'))
