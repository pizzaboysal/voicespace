import firebase_admin
from firebase_admin import credentials, firestore

<<<<<<< HEAD
# Path to your Firebase service account key
cred = credentials.Certificate("firebase_key.json")

# Initialize the app only once
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

# Firestore database client
=======
# Only initialize if it hasn't been initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

# Get Firestore client
>>>>>>> e789cb459b0f7bc67d8db1c4e5102b78d285071b
db = firestore.client()
