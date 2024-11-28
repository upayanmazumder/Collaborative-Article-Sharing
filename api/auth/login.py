from flask import Blueprint, request, jsonify
from firebase_admin import auth

login_bp = Blueprint('login', __name__)

@login_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        # Get the email from the request (no password needed for Firebase login)
        email = request.json.get('email')

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        # Verify if the user exists in Firebase
        user = auth.get_user_by_email(email)

        # Generate a custom token for the user
        custom_token = auth.create_custom_token(user.uid)

        return jsonify({
            'customToken': custom_token.decode("utf-8"),  # Decode the custom token to a string
        }), 200

    except auth.UserNotFoundError:
        return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 400
