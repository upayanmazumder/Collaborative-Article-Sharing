from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore

privacy_group_bp = Blueprint('privacy_group', __name__)
db = firestore.client()

@privacy_group_bp.route('/auth/group/privacy', methods=['PATCH'])
def set_privacy():
    """
    Route to set a group's privacy (private or public). Only the group creator can update the privacy.
    """
    id_token = request.headers.get('Authorization')

    if not id_token:
        return jsonify({"error": "Missing Firebase ID token"}), 401

    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        group_data = request.json
        if not group_data or 'group_id' not in group_data or 'privacy' not in group_data:
            return jsonify({"error": "Missing 'group_id' or 'privacy' in request body"}), 400

        group_id = group_data['group_id']
        privacy = group_data['privacy'].lower()

        if privacy not in ['private', 'public']:
            return jsonify({"error": "Invalid privacy value. Must be 'private' or 'public'"}), 400

        group_ref = db.collection('groups').document(group_id)
        group = group_ref.get()

        if not group.exists:
            return jsonify({"error": "Group not found"}), 404

        group_data = group.to_dict()

        if group_data['created_by'] != user_id:
            return jsonify({"error": "Only the group creator can update the privacy"}), 403

        group_ref.update({"privacy": privacy})
        return jsonify({"success": True, "message": f"Group privacy set to {privacy}"}), 200

    except auth.InvalidIdTokenError:
        return jsonify({"error": "Invalid Firebase ID token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
