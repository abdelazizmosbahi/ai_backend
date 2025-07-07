# Import os and dotenv to load environment variables
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration class for the Flask application
class Config:
    # MongoDB URI, defaults to local AskSphere database if not set in .env
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/asksphere_ai')
    # Secret key for Flask, defaults to a secure value if not set in .env
    SECRET_KEY = os.getenv('SECRET_KEY', 'b96aaa7e5d3e3a962ac0e58ae86d7c0779413b53745b636a18ce23ed2eb6ae1f')
    # Azure Cognitive Services endpoint and key (placeholders for chatbot integration)
    AZURE_LANGUAGE_ENDPOINT = os.getenv('AZURE_LANGUAGE_ENDPOINT', 'https://<your-resource-name>.cognitiveservices.azure.com/')
    AZURE_LANGUAGE_KEY = os.getenv('AZURE_LANGUAGE_KEY', '<your-azure-key>')