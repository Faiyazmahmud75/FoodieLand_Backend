import firebase_admin
from firebase_admin import credentials, auth
import os

FIREBASE_CRED_PATH = os.path.join(os.path.dirname(__file__), 'firebase_service_account.json')

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    default_app = firebase_admin.initialize_app(cred, {
        'authDomain': 'foodieland-3fd9e.firebaseapp.com',
    })