"""
Generates a signed license JSON using a private RSA key.
Usage:
python generate_license.py --customer "ristorante-roma" --out license.json
"""
import argparse
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


PRIVATE_KEY_PATH = 'private_key.pem'


parser = argparse.ArgumentParser()
parser.add_argument('--customer', required=True)
parser.add_argument('--out', default='license.json')
args = parser.parse_args()


payload = {
'customer_id': args.customer,
'type': 'self',
'issued_at': __import__('datetime').datetime.utcnow().isoformat()
}


with open(PRIVATE_KEY_PATH, 'rb') as kf:
    priv = serialization.load_pem_private_key(kf.read(), password=None)


s = json.dumps(payload, sort_keys=True).encode()
sig = priv.sign(s, padding.PKCS1v15(), hashes.SHA256())
payload['__sig'] = sig.hex()
with open(args.out, 'w') as f:
    json.dump(payload, f, indent=2)
print('Wrote', args.out)