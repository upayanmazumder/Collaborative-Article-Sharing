import os

API_URL = "https://api.cas.upayan.dev"
APP_URL = "https://cas.upayan.dev"

if os.getenv("ENV") == "development":
    API_URL = "http://localhost:4000"
    APP_URL = "http://localhost:3000"
