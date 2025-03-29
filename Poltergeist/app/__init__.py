from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-replace-in-prod')
    
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app 