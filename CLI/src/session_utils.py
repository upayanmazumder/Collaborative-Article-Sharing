import os
import json
import re

session_file = "session.json"

def load_session_details():
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            return json.load(f)
    return {}

def save_session_details(details):
    with open(session_file, "w") as f:
        json.dump(details, f)

def is_valid_url(url):
    url_regex = re.compile(
        r'^(https?:\/\/)?'
        r'([\da-z\.-]+)\.([a-z\.]{2,6})'
        r'([\/\w \.-]*)*\/?$'
    )
    return re.match(url_regex, url) is not None
