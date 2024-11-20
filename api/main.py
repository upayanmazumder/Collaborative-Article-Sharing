from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://api.collaborative-article-sharing.upayan.dev/"])

@app.route('/')
def home():
    return "Welcome to the API server!"

if __name__ == '__main__':
    app.run(debug=True, port=3000)