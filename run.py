# from app import create_app

# app = create_app()
# if __name__ == '__main__':
#        app.run(debug=True)


from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensure the notifications collection exists (no need to drop unless resetting)
        if app.mongo.db.notifications.count_documents({}) == 0:
            print("Notifications collection initialized.")
    
    app.run(debug=True, port=5001)