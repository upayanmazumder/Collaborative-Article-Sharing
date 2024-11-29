# FILE: auth/group/list.py
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

list_group_bp = Blueprint('list_group', __name__)

db = firestore.client()

@list_group_bp.route('/auth/group/list', methods=['GET'])
def list_groups():
    """
    Route to retrieve the list of public groups. Optionally filter by user email if a 'user' query parameter is provided.
    """
    try:
        # Get the optional 'user' query parameter
        user_email = request.args.get('user')

        # Query Firestore for public groups
        groups_ref = db.collection('groups').where("privacy", "==", "public")
        public_groups = groups_ref.stream()

        groups_list = []
        for group in public_groups:
            group_data = group.to_dict()
            if user_email:
                # If filtering by user email, only include groups where the user is a member
                if user_email in group_data.get('members', []):
                    groups_list.append({"id": group.id, **group_data})
            else:
                # Include all public groups if no user filter is applied
                groups_list.append({"id": group.id, **group_data})

        return jsonify({
            "success": True,
            "groups": groups_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
