from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Wgg"

if __name__ == '__main__':
    cert_path = '/root/docker/cas/cert.pem'
    key_path = '/root/docker/cas/key.pem'
    
    app.run(debug=True, port=3000, ssl_context=(cert_path, key_path))
