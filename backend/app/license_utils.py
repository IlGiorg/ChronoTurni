import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os


# Simple utilities to verify a signed JSON license file using RSA public key


PUBLIC_KEY_PATH = os.environ.get('PUBLIC_KEY_PATH', '/app/public_key.pem')


def verify_license_file(path: str) -> dict:
    with open(path, 'rb') as f:
        data = json.load(f)
    signature = bytes.fromhex(data.pop('__sig'))
    payload = json.dumps(data, sort_keys=True).encode()
    with open(PUBLIC_KEY_PATH, 'rb') as kf:
        pub = serialization.load_pem_public_key(kf.read())
    try:
        pub.verify(
            signature,
            payload,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return data
    except Exception as e:
        raise ValueError('Invalid license signature')

import requests

GITHUB_AUTH_BASE = "https://raw.githubusercontent.com/ilgiorg/chronoturni/licenses/auth"

def validate_customer(customer_id: str):
    url = f"{GITHUB_AUTH_BASE}/{customer_id}.json"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return False, "License not found"
        data = res.json()
        if not data.get("valid", False):
            return False, "License revoked"
        return True, "License OK"
    except Exception as e:
        return False, f"Error validating license: {e}"
