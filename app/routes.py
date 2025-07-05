# from flask import Blueprint, jsonify, request
# from app.models import create_notification, get_user_notifications
# from app.notification_logic import prioritize_notification
# from app import mongo  # Import mongo, which will be set after create_app

# bp = Blueprint('main', __name__)

#    # Existing routes (keep your original routes here)
#    # Append new notification routes
# @bp.route('/api/notifications', methods=['POST'])
# def add_notification():
#        data = request.get_json()
#        user_id = data.get('user_id')
#        notification_type = data.get('type')
#        content = data.get('content')
#        priority = prioritize_notification(notification_type)

#        if not all([user_id, notification_type, content]):
#            return jsonify({'error': 'Missing required fields'}), 400

#        result = create_notification(mongo, user_id, notification_type, content, priority)
#        return jsonify({'message': 'Notification created', 'id': str(result.inserted_id)}), 201

# @bp.route('/api/notifications/<user_id>', methods=['GET'])
# def fetch_notifications(user_id):
#         limit = request.args.get('limit', default=10, type=int)
#         notifications = get_user_notifications(mongo, user_id, limit)
#         return jsonify([{
#             'id': str(n['_id']),
#             'type': n['type'],
#             'content': n['content'],
#             'priority': n['priority'],
#             'timestamp': n['timestamp'].isoformat(),
#             'read': n['read']
#         } for n in notifications]), 200


from flask import Blueprint, jsonify, request, current_app
from app.models import create_notification, get_user_notifications
from app.notification_logic import prioritize_notification

bp = Blueprint('main', __name__)

@bp.route('/notifications', methods=['POST'])
def add_notification():
    data = request.get_json()
    user_id = data.get('user_id')
    notification_type = data.get('type')
    content = data.get('content')
    priority = prioritize_notification(notification_type)

    if not all([user_id, notification_type, content]):
        return jsonify({'error': 'Missing required fields'}), 400

    with current_app.app_context():
        result = create_notification(current_app.mongo, user_id, notification_type, content, priority)
        return jsonify({'message': 'Notification created', 'id': str(result.inserted_id)}), 201

@bp.route('/notifications/<user_id>', methods=['GET'])
def fetch_notifications(user_id):
    limit = request.args.get('limit', default=10, type=int)
    with current_app.app_context():
        notifications = get_user_notifications(current_app.mongo, user_id, limit)
        return jsonify([{
            'id': str(n['_id']),
            'type': n['type'],
            'content': n['content'],
            'priority': n['priority'],
            'timestamp': n['timestamp'].isoformat(),
            'read': n['read']
        } for n in notifications]), 200