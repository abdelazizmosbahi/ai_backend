def prioritize_notification(notification_type):
         priority_map = {
             'ban': 'high',
             'question_response': 'high',
             'badge_awarded': 'medium',
             'vote': 'low'
         }
         return priority_map.get(notification_type, 'medium')