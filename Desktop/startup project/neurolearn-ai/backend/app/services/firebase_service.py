import firebase_admin
from firebase_admin import credentials, auth
from app.config import settings
from loguru import logger
from typing import Dict, Any

firebase_app = None


def initialize_firebase():
    global firebase_app
    try:
        if not firebase_app:
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": settings.firebase_project_id,
                "private_key_id": settings.firebase_private_key_id,
                "private_key": settings.firebase_private_key.replace("\\n", "\n"),
                "client_email": settings.firebase_client_email,
                "client_id": settings.firebase_client_id,
                "auth_uri": settings.firebase_auth_uri,
                "token_uri": settings.firebase_token_uri,
                "auth_provider_x509_cert_url": settings.firebase_auth_provider_x509_cert_url,
                "client_x509_cert_url": settings.firebase_client_x509_cert_url + settings.firebase_client_id,
            })
            firebase_app = firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Firebase initialization failed: {e}")
        raise


async def verify_firebase_token(id_token: str) -> Dict[str, Any]:
    try:
        if not firebase_app:
            initialize_firebase()
        
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logger.error(f"Firebase token verification failed: {e}")
        raise
