# FILE: auth/group/create.py
from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore

create_group_bp = Blueprint('create_group', __name__)

db = firestore.client()

@create_group_bp.route('/auth/group/create', methods=['POST'])
def create_group():
    """
    Route to create a new group. The user must be authenticated using a Firebase token.
    """
    # Retrieve the Firebase ID token from the Authorization header
    id_token = request.headers.get('Authorization')

    if not id_token:
        return jsonify({"error": "Missing Firebase ID token"}), 401

    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        # Retrieve the authenticated user's email
        user_email = decoded_token.get('email')
        if not user_email:
            return jsonify({"error": "Unable to retrieve user email from token"}), 401

        # Get the group name from the request body
        group_data = request.json
        if not group_data or 'group_name' not in group_data:
            return jsonify({"error": "Missing 'group_name' in request body"}), 400

        group_name = group_data['group_name']
        description = group_data.get('description')  # Optional field

        group_id = db.collection('groups').document().id

        # Prepare the group entry
        group_entry = {
            "group_name": group_name,
            "description": description,
            "group_leader": user_email,  # Store the creator's email as the group leader
            "created_by": user_id,
            "created_at": firestore.SERVER_TIMESTAMP,
            "members": [user_email]  # Add the creator's email as the first member
        }

        # Save the group in Firestore
        group_ref = db.collection('groups').document(group_id)
        group_ref.set(group_entry)

        return jsonify({
            "success": True,
            "group_id": group_id,
            "message": "Group created successfully"
        }), 201

    except auth.InvalidIdTokenError:
        return jsonify({"error": "Invalid Firebase ID token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
