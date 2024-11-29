import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv

# Load environment variables from the .env file
if load_dotenv():
    print(".env file loaded successfully.")
else:
    print("No .env file found or failed to load. Ensure environment variables are set.")

# List of required environment variables for Firebase
required_env_vars = [
    "FIREBASE_PROJECT_ID",
    "FIREBASE_PRIVATE_KEY_ID",
    "FIREBASE_PRIVATE_KEY",
    "FIREBASE_CLIENT_EMAIL",
    "FIREBASE_CLIENT_ID",
    "FIREBASE_AUTH_URI",
    "FIREBASE_TOKEN_URI",
    "FIREBASE_AUTH_PROVIDER_CERT_URL",
    "FIREBASE_CLIENT_CERT_URL"
]

# Check for missing environment variables
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    exit(1)  # Exit the application if critical variables are missing

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Load Firebase credentials from environment variables
firebase_credentials = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
}

try:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

    # Initialize Firestore
    db = firestore.client()
    print("Firebase Admin SDK initialized successfully.")

except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    db = None  # Graceful fallback if Firebase initialization fails

# Import and register blueprints
try:
    from auth.signup import signup_bp
    from auth.login import login_bp

    app.register_blueprint(signup_bp)
    app.register_blueprint(login_bp)
    print("Auth blueprints registered successfully.")
except ImportError as e:
    print(f"Error importing blueprints: {e}")


@app.route('/')
def home():
    return "Welcome to the Flask App"


@app.route('/push', methods=['POST'])
def add_article():
    """
    Route to add a article to the user's data.
    Requires the user to be authenticated using a Firebase token.
    """
    # Retrieve the Firebase ID token from the Authorization header
    id_token = request.headers.get('Authorization')

    if not id_token:
        return jsonify({"error": "Missing Firebase ID token"}), 401

    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        # Get the article from the request body
        article_data = request.json
        if not article_data or 'article' not in article_data:
            return jsonify({"error": "Missing 'article' in request body"}), 400

        article = article_data['article']

        # Store the article in Firestore under the user's collection
        if db:
            user_ref = db.collection('users').document(user_id)
            user_ref.update({
                'articles': firestore.ArrayUnion([article])
            })
            return jsonify({"success": True, "article": "article added successfully"}), 200
        else:
            return jsonify({"error": "Firestore database is not initialized"}), 500
    except auth.InvalidIdTokenError:
        return jsonify({"error": "Invalid Firebase ID token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv("PORT", 3000))  # Default to port 3000 if not specified
    app.run(debug=True, port=port)
