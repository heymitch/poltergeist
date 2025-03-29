from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import json
import os
from datetime import datetime

class User:
    def __init__(self):
        self.users_file = 'data/users.json'
        self._ensure_data_file()
        
    def _ensure_data_file(self):
        """Ensure the users data file exists"""
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def _load_users(self):
        """Load users from JSON file"""
        with open(self.users_file, 'r') as f:
            return json.load(f)

    def _save_users(self, users):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

    def create_user(self, email, password, invite_code):
        """Create a new user with the given invite code"""
        users = self._load_users()
        
        # Check if user already exists
        if email in users:
            raise ValueError("User already exists")
            
        # Verify invite code
        if not self.verify_invite_code(invite_code):
            raise ValueError("Invalid invitation code")
            
        # Create new user
        users[email] = {
            'password_hash': generate_password_hash(password),
            'created_at': datetime.utcnow().isoformat(),
            'invite_code_used': invite_code,
            'nda_accepted': False
        }
        
        self._save_users(users)
        return True

    def verify_credentials(self, email, password):
        """Verify user credentials"""
        users = self._load_users()
        user = users.get(email)
        
        if user and check_password_hash(user['password_hash'], password):
            return True
        return False

    def has_accepted_nda(self, email):
        """Check if user has accepted NDA"""
        users = self._load_users()
        user = users.get(email)
        return user and user.get('nda_accepted', False)

    def accept_nda(self, email):
        """Mark NDA as accepted for user"""
        users = self._load_users()
        if email not in users:
            return False
        
        users[email]['nda_accepted'] = True
        users[email]['nda_accepted_at'] = datetime.utcnow().isoformat()
        self._save_users(users)
        return True

    def generate_invite_code(self):
        """Generate a new invitation code"""
        code = secrets.token_urlsafe(16)
        users = self._load_users()
        
        if 'invite_codes' not in users:
            users['invite_codes'] = {}
            
        users['invite_codes'][code] = {
            'created_at': datetime.utcnow().isoformat(),
            'used': False
        }
        
        self._save_users(users)
        return code

    def verify_invite_code(self, code):
        """Verify if an invite code is valid and unused"""
        users = self._load_users()
        invite_codes = users.get('invite_codes', {})
        
        if code in invite_codes and not invite_codes[code]['used']:
            invite_codes[code]['used'] = True
            self._save_users(users)
            return True
        return False 