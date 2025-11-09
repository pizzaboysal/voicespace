import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase service account key
cred = credentials.Certificate("firebase_key.json")

# Initialize the app only once
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

# Firestore database client
db = firestore.client()
