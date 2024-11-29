from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore

delete_group_bp = Blueprint('delete_group', __name__)
db = firestore.client()

@delete_group_bp.route('/auth/group/delete', methods=['DELETE'])
def delete_group():
    """
    Route to delete a group. Only the group creator can delete the group.
    """
    id_token = request.headers.get('Authorization')

    if not id_token:
        return jsonify({"error": "Missing Firebase ID token"}), 401

    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        group_data = request.json
        if not group_data or 'group_id' not in group_data:
            return jsonify({"error": "Missing 'group_id' in request body"}), 400

        group_id = group_data['group_id']
        group_ref = db.collection('groups').document(group_id)
        group = group_ref.get()

        if not group.exists:
            return jsonify({"error": "Group not found"}), 404

        group_data = group.to_dict()

        if group_data['created_by'] != user_id:
            return jsonify({"error": "Only the group creator can delete the group"}), 403

        group_ref.delete()
        return jsonify({"success": True, "message": "Group deleted successfully"}), 200

    except auth.InvalidIdTokenError:
        return jsonify({"error": "Invalid Firebase ID token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
