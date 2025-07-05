# from flask import Flask
# from flask_pymongo import PyMongo
# from app.config import Config

# mongo = None  # Placeholder until initialized

# def create_app():
#        global mongo
#        app = Flask(__name__)
#        app.config.from_object(Config)
       
#        # Initialize MongoDB
#        mongo = PyMongo(app)
       
#        # Import routes after mongo initialization
#        from app.routes import bp
#        app.register_blueprint(bp)
       
#        return app

from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoDB and attach it to the app
    app.mongo = PyMongo(app)
    
    # Import routes after mongo initialization
    from app.routes import bp
    app.register_blueprint(bp, url_prefix='/api')
    
    return app