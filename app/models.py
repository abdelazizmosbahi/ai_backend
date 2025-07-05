from datetime import datetime

def create_notification(mongo, user_id, notification_type, content, priority='medium'):
        notification = {
            'user_id': user_id,
            'type': notification_type,
            'content': content,
            'priority': priority,
            'timestamp': datetime.utcnow(),
            'read': False
        }
        return mongo.db.notifications.insert_one(notification)

def get_user_notifications(mongo, user_id, limit=10):
        return list(mongo.db.notifications.find({'user_id': user_id, 'read': False})
                    .sort('timestamp', -1)
                    .limit(limit))

    # Add your existing model definitions here