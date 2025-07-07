# Import the create_app function from the app module to initialize the Flask application
from app import create_app

# Create the Flask application instance
app = create_app()

# Main entry point for running the application
if __name__ == '__main__':
    with app.app_context():
        # Ensure the notifications collection exists in MongoDB
        # Only print initialization message if the collection is empty
        if app.mongo.db.notifications.count_documents({}) == 0:
            print("Notifications collection initialized.")
    
    # Run the Flask app in debug mode on port 5001
    app.run(debug=True, port=5001)