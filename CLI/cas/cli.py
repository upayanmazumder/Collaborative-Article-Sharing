from flask import Flask
import webbrowser
from auth import auth_bp

app = Flask(__name__)

# Register the auth blueprint
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    url = "https://cas.upayan.dev/auth/connect?redirect_uri=http://localhost:8000"
    webbrowser.open(url)
    print("Starting server on http://localhost:8000")
    app.run(port=8000)
