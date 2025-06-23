import os
import json
import firebase_admin
from firebase_admin import credentials, auth

# Read credentials from environment variable (JSON string)
firebase_cred_json = os.getenv("FIREBASE_CRED_JSON")

if firebase_cred_json is None:
    raise ValueError("Missing FIREBASE_CRED_JSON environment variable")

cred = credentials.Certificate(json.loads(firebase_cred_json))
firebase_admin.initialize_app(cred)

def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return None
