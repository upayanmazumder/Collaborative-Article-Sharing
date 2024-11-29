from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore

privacy_group_bp = Blueprint('privacy_group', __name__)
db = firestore.client()

@privacy_group_bp.route('/auth/group/privacy', methods=['PATCH'])
def update_group_privacy():
    id_token = request.headers.get('Authorization')
    if not id_token:
        return jsonify({"error": "Missing Firebase ID token"}), 401

    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        data = request.json
        group_id = data.get("group_id")
        privacy = data.get("privacy")

        if not group_id or not privacy:
            return jsonify({"error": "Missing 'group_id' or 'privacy' in request body"}), 400

        if privacy not in ["private", "public"]:
            return jsonify({"error": "Invalid privacy setting"}), 400

        group_ref = db.collection('groups').document(group_id)
        group_data = group_ref.get()

        if group_data.exists and group_data.to_dict().get("created_by") == user_id:
            group_ref.update({"privacy": privacy})
            return jsonify({"success": True, "message": "Group privacy updated"}), 200
        else:
            return jsonify({"error": "Group not found or insufficient permissions"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500
