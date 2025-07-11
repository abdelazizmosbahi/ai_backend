# Import os and dotenv to load environment variables
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration class for the Flask application
class Config:
    # MongoDB URI, defaults to local AskSphere database if not set in .env
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://mosbehiasiz:BSvss3YfLyb0ojMa@cluster0.ntfhykc.mongodb.net/asksphere?retryWrites=true&w=majority')
    # Secret key for Flask, defaults to a secure value if not set in .env
    SECRET_KEY = os.getenv('SECRET_KEY', '9035aa297aca23fca3b5f070fe909e01567739b99fa41a55bb6ad63076a0adf9')
    # Azure Cognitive Services endpoint and key (placeholders for chatbot integration)
    AZURE_LANGUAGE_ENDPOINT = os.getenv('AZURE_LANGUAGE_ENDPOINT', 'https://<your-resource-name>.cognitiveservices.azure.com/')
    AZURE_LANGUAGE_KEY = os.getenv('AZURE_LANGUAGE_KEY', '<your-azure-key>')