import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

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

# Initialize Firebase Admin SDK with the credentials from the environment variables
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

@app.route('/')
def home():
    return "Wgg"

@app.route('/auth/signup', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True, port=3000)
