# FILE: auth/login.py
from flask import Blueprint, request, jsonify
from firebase_admin import auth

login_bp = Blueprint('login', __name__)

@login_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        # Get the email and password from the request
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Verify the user using Firebase Authentication
        user = auth.get_user_by_email(email)

        # Here you would typically verify the password and generate a token
        # For simplicity, we assume the password is correct and return user info

        return jsonify({
            'uid': user.uid,
            'email': user.email
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400