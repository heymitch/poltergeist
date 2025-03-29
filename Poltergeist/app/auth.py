from functools import wraps
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from .models.user import User

auth = Blueprint('auth', __name__)
user_model = User()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('auth.login'))
        
        # Check if NDA is accepted
        if not user_model.has_accepted_nda(session['user_email']):
            return redirect(url_for('auth.nda'))
            
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if user_model.verify_credentials(email, password):
            session['user_email'] = email
            
            # Check if NDA needs to be accepted
            if not user_model.has_accepted_nda(email):
                return jsonify({'redirect': url_for('auth.nda')})
            
            return jsonify({'redirect': url_for('main.index')})
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('auth/login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        invite_code = data.get('invite_code')
        
        try:
            user_model.create_user(email, password, invite_code)
            session['user_email'] = email
            return jsonify({'redirect': url_for('auth.nda')})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('auth/signup.html')

@auth.route('/nda', methods=['GET', 'POST'])
def nda():
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        data = request.get_json()
        if data.get('accept'):
            user_model.accept_nda(session['user_email'])
            return jsonify({'redirect': url_for('main.index')})
        return jsonify({'error': 'NDA must be accepted to continue'}), 400
    
    return render_template('auth/nda.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# Admin route for generating invite codes (should be protected in production)
@auth.route('/admin/invite', methods=['POST'])
def generate_invite():
    code = user_model.generate_invite_code()
    return jsonify({'invite_code': code}) 