# FILE: auth/signup.py
from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore

signup_bp = Blueprint('signup', __name__)

db = firestore.client()

@signup_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        # Get the email and password from the request
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Create a new user using Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )

        # Store user data in Firestore
        user_ref = db.collection('users').document(user.uid)
        user_ref.set({
            'email': user.email,
            'uid': user.uid,
            'created_at': firestore.SERVER_TIMESTAMP
        })

        # Return success response
        return jsonify({
            'uid': user.uid,
            'email': user.email
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400