import os
import firebase_admin
from firebase_admin import credentials, auth

# Dynamically get the path to the JSON file in the same directory as this script
json_path = os.path.join(os.path.dirname(__file__), 'fsd-task-tracker-app-firebase-adminsdk-fbsvc-25b77c8307.json')
cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred)

def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return None