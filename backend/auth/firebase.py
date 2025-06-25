import os
import json
import firebase_admin
from firebase_admin import credentials, auth
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Read credentials from environment variable (JSON string)
firebase_cred_json = os.getenv("FIREBASE_CRED_JSON")

if firebase_cred_json is None:
    raise ValueError("Missing FIREBASE_CRED_JSON environment variable")

logging.info("Initializing Firebase Admin SDK...")
cred = credentials.Certificate(json.loads(firebase_cred_json))
firebase_admin.initialize_app(cred)
logging.info("Firebase Admin SDK initialized.")

def verify_firebase_token(token: str):
    try:
        logging.info("Verifying Firebase token...")
        decoded_token = auth.verify_id_token(token)
        logging.info("Firebase token verified successfully.")
        return decoded_token
    except Exception as e:
        logging.error(f"Failed to verify Firebase token: {e}")
        return None
