from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(allowed_roles):
    """
    Decorator to restrict access to routes based on user roles.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            
            user_role = session.get('role')
            if user_role not in allowed_roles:
                # Optional: Add a flash message for feedback
                # flash('Acesso negado: você não tem permissão para acessar esta página.')
                return redirect(url_for('project.dashboard'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
