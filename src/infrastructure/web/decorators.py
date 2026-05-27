from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))

            user_role = session.get('role')
            if user_role not in allowed_roles:
                return redirect(url_for('project.dashboard'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
