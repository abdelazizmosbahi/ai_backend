# Define a function to prioritize notifications based on their type
def prioritize_notification(notification_type):
    # Mapping of notification types to their priority levels
    priority_map = {
        'ban': 'high',
        'question_response': 'high',
        'badge_awarded': 'medium',
        'vote': 'low',
        'restriction_warning': 'medium',
        'chatbot_response': 'medium'  # Added for chatbot responses
    }
    return priority_map.get(notification_type, 'medium')