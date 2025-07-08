from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoDB
    app.mongo = PyMongo(app)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:4200", "https://your-frontend-domain.com"]}})
    
    # Import routes
    from app.routes import bp
    app.register_blueprint(bp, url_prefix='/api')
    
    return app