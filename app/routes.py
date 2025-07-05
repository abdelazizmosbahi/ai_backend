from flask import Blueprint, jsonify, request, current_app
from app.models import create_notification, get_user_notifications, log_violation, update_user_restriction, check_and_enforce_ban
from app.notification_logic import prioritize_notification
from detoxify import Detoxify

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

@bp.route('/moderate', methods=['POST'])
def moderate_content():
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')
    if not all([user_id, content]):
        return jsonify({'error': 'Missing user_id or content'}), 400

    with current_app.app_context():
        # Analyze content with Detoxify
        results = Detoxify('original').predict(content)
        toxicity_score = float(results['toxicity'])  # Convert np.float32 to float

        response = {
            'user_id': user_id,
            'content': content,
            'toxicity_score': toxicity_score
        }

        # Check for toxicity (threshold > 0.9)
        if toxicity_score > 0.9:
            log_violation(current_app.mongo, user_id, content, toxicity_score)
            updated_user = update_user_restriction(current_app.mongo, user_id)
            new_restriction_level = updated_user.get('restrictionLevel', 1)  # Default to 1 if not set
            # Send restriction warning notification
            warning_content = f"Your restriction level has increased to {new_restriction_level}. Further violations (5 total) may lead to a ban."
            create_notification(current_app.mongo, user_id, 'restriction_warning', warning_content, 'medium')
            if check_and_enforce_ban(current_app.mongo, user_id):
                response['action'] = 'banned'
            else:
                response['action'] = 'restriction_increased'
                violation_count = current_app.mongo.db.violations.count_documents({'user_id': user_id})
                response['violation_count'] = violation_count
        else:
            response['action'] = 'approved'

        return jsonify(response), 200