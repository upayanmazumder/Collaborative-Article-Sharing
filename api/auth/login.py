from flask import Blueprint, request, jsonify
from firebase_admin import auth
import urllib.parse

login_bp = Blueprint("login", __name__)

@login_bp.route("/auth/login", methods=["POST"])
def login():
    try:
        # Get the email from the request
        email = request.json.get("email")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Verify if the user exists in Firebase
        user = auth.get_user_by_email(email)

        # Generate a one-time login URL
        action_code_settings = {
            "url": "http://localhost:8000/",
            "handleCodeInApp": False,
        }
        login_url = auth.generate_email_action_link("SIGN_IN", email, action_code_settings)

        return jsonify({"loginUrl": urllib.parse.quote(login_url)}), 200

    except auth.UserNotFoundError:
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400
