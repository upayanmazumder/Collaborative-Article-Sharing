from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore

delete_group_bp = Blueprint('delete_group', __name__)
db = firestore.client()

@delete_group_bp.route('/auth/group/delete', methods=['DELETE'])
def delete_group():
    id_token = request.headers.get('Authorization')
    if not id_token:
        return jsonify({"error": "Missing Firebase ID token"}), 401

    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        group_id = request.json.get("group_id")
        if not group_id:
            return jsonify({"error": "Missing 'group_id' in request body"}), 400

        group_ref = db.collection('groups').document(group_id)
        group_data = group_ref.get()

        if group_data.exists and group_data.to_dict().get("created_by") == user_id:
            group_ref.delete()
            return jsonify({"success": True, "message": "Group deleted successfully"}), 200
        else:
            return jsonify({"error": "Group not found or insufficient permissions"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500
