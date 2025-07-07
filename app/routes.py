# Import necessary Flask modules and project dependencies
from flask import Blueprint, jsonify, request, current_app
from app.models import (
    create_notification, get_user_notifications, log_violation,
    update_user_restriction, check_and_enforce_ban, log_chat_interaction
)
from app.notification_logic import prioritize_notification
from app.services import handle_chat_query  # Import chatbot query handler
from detoxify import Detoxify
import logging  # For debug logging

# Set up logging to debug query processing
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask Blueprint for the main routes
bp = Blueprint('main', __name__)

# Endpoint to create a new notification
@bp.route('/notifications', methods=['POST'])
def add_notification():
    data = request.get_json()
    user_id = data.get('user_id')
    notification_type = data.get('type')
    content = data.get('content')
    priority = prioritize_notification(notification_type)

    if not all([user_id, notification_type, content]):
        logger.error("Missing required fields in notification request")
        return jsonify({'error': 'Missing required fields'}), 400

    with current_app.app_context():
        result = create_notification(current_app.mongo, user_id, notification_type, content, priority)
        logger.debug(f"Notification created with ID: {result.inserted_id}")
        return jsonify({'message': 'Notification created', 'id': str(result.inserted_id)}), 201

# Endpoint to fetch notifications for a user
@bp.route('/notifications/<user_id>', methods=['GET'])
def fetch_notifications(user_id):
    limit = request.args.get('limit', default=10, type=int)
    with current_app.app_context():
        notifications = get_user_notifications(current_app.mongo, user_id, limit)
        logger.debug(f"Fetched {len(notifications)} notifications for user {user_id}")
        return jsonify([{
            'id': str(n['_id']),
            'type': n['type'],
            'content': n['content'],
            'priority': n['priority'],
            'timestamp': n['timestamp'].isoformat(),
            'read': n['read']
        } for n in notifications]), 200

# Endpoint to moderate content using Detoxify
@bp.route('/moderate', methods=['POST'])
def moderate_content():
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')
    if not all([user_id, content]):
        logger.error("Missing user_id or content in moderation request")
        return jsonify({'error': 'Missing user_id or content'}), 400

    with current_app.app_context():
        # Analyze content with Detoxify
        results = Detoxify('original').predict(content)
        toxicity_score = float(results['toxicity'])  # Convert np.float32 to float
        logger.debug(f"Content moderation for user {user_id}: toxicity_score={toxicity_score}")

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
                logger.debug(f"User {user_id} banned due to violations")
            else:
                response['action'] = 'restriction_increased'
                violation_count = current_app.mongo.db.violations.count_documents({'user_id': user_id})
                response['violation_count'] = violation_count
                logger.debug(f"User {user_id} restriction level increased to {new_restriction_level}")
        else:
            response['action'] = 'approved'
            logger.debug(f"Content approved for user {user_id}")

        return jsonify(response), 200

# Endpoint for the User Support Chatbot
@bp.route('/chatbot', methods=['POST'])
def chatbot_interaction():
    # Get JSON data from the request
    data = request.get_json()
    user_id = data.get('user_id')
    query = data.get('query')
    
    if not all([user_id, query]):
        logger.error("Missing user_id or query in chatbot request")
        return jsonify({'error': 'Missing user_id or query'}), 400

    with current_app.app_context():
        try:
            # Process the query using the handle_chat_query function from services
            response_text = handle_chat_query(current_app.mongo, user_id, query)
            
            # Create a notification for the chatbot response
            create_notification(
                current_app.mongo,
                user_id,
                'chatbot_response',
                f"Chatbot: {response_text}",
                prioritize_notification('chatbot_response')
            )
            
            # Prepare response
            response = {
                'user_id': user_id,
                'query': query,
                'response': response_text
            }
            logger.debug(f"Chatbot response for user {user_id}: {response_text}")
            return jsonify(response), 200
        
        except Exception as e:
            # Handle errors gracefully
            logger.error(f"Chatbot processing failed: {str(e)}")
            return jsonify({'error': f'Chatbot processing failed: {str(e)}'}), 500