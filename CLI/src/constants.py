import os

API_URL = "https://api.cas.upayan.dev"
if os.getenv("ENV") == "development":
    API_URL = "http://localhost:4000"