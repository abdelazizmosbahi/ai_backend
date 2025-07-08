# Import datetime for timestamp handling
from datetime import datetime

# Function to create a notification in the MongoDB notifications collection
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

# Function to retrieve all notifications for a user, sorted by timestamp
def get_user_notifications(mongo, user_id, limit=10):
    return list(mongo.db.notifications.find({'user_id': user_id})
                .sort('timestamp', -1)
                .limit(limit))

# Function to log a violation in the MongoDB violations collection
def log_violation(mongo, user_id, content, toxicity_score):
    violation = {
        'user_id': user_id,
        'content': content,
        'toxicity_score': float(toxicity_score),  # Convert np.float32 to float
        'timestamp': datetime.utcnow()
    }
    return mongo.db.violations.insert_one(violation)

# Function to increment a user's restriction level
def update_user_restriction(mongo, user_id, increment=1):
    user = mongo.db.users.find_one_and_update(
        {'_id': user_id},
        {'$inc': {'restrictionLevel': increment}},
        upsert=True,
        return_document=True
    )
    return user

# Function to check if a user should be banned based on violation count
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

# Function to log chatbot interactions for analytics
def log_chat_interaction(mongo, user_id, query, response):
    interaction = {
        'user_id': user_id,
        'query': query,
        'response': response,
        'timestamp': datetime.utcnow()
    }
    return mongo.db.chatbot_interactions.insert_one(interaction)

# Function to retrieve questions and communities from MongoDB
def get_questions_and_communities(mongo):
    questions = list(mongo.db.questions.find())
    communities = list(mongo.db.communities.find())
    return questions, communities