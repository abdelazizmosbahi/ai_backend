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

# second ai agent

def log_violation(mongo, user_id, content, toxicity_score):
    violation = {
        'user_id': user_id,
        'content': content,
        'toxicity_score': float(toxicity_score),  # Convert np.float32 to float
        'timestamp': datetime.utcnow()
    }
    return mongo.db.violations.insert_one(violation)

def update_user_restriction(mongo, user_id, increment=1):
    user = mongo.db.users.find_one_and_update(
        {'_id': user_id},
        {'$inc': {'restrictionLevel': increment}},
        upsert=True,
        return_document=True
    )
    return user

def check_and_enforce_ban(mongo, user_id):
    violations = mongo.db.violations.count_documents({'user_id': user_id})
    if violations >= 5:
        mongo.db.users.update_one(
            {'_id': user_id},
            {'$set': {'status': 'banned', 'community_bans': {'all': True}}},
            upsert=True
        )
        create_notification(mongo, user_id, 'ban', 'You have been permanently banned due to multiple violations.')
        return True
    return False