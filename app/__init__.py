# Import Flask and PyMongo for application and database setup
from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config

# Function to create and configure the Flask application
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoDB and attach it to the app
    app.mongo = PyMongo(app)
    
    # Import routes after MongoDB initialization
    from app.routes import bp
    app.register_blueprint(bp, url_prefix='/api')
    
    return app