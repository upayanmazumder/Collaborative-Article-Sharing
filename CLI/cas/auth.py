from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)
session_details = {}

@auth_bp.route("/")
def handle_auth_response():
    global session_details
    email = request.args.get("email", "")
    token = request.args.get("token", "")

    # Only update session details if email and token are present
    if email and token:
        session_details = {
            "email": email,
            "token": token
        }
        print("Session details saved:", session_details)
    else:
        print("Invalid or empty session details, skipping update.")

    return jsonify({"status": "ok", "session_details": session_details})


@auth_bp.route("/favicon.ico")
def favicon():
    return "", 200  # Prevent favicon requests from interfering
