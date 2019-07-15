import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

from ..formatters import encode_sig, decode_sig
from ...convert import int_to_hex_str
from .common import point_to_hex_str
from .errors import (
    UnknownPointFormatError, UnknownSignatureFormatError,
    UnknownPublicKeyFormatError
)

logger = logging.getLogger(__name__)
backend_name = 'cryptography'
backend = default_backend()

class CurveByAttrName:
    @property
    def P256(self):
        return ec.SECP256R1()

curve = CurveByAttrName()
sha256 = hashes.SHA256()

def gen_private_key(curve=curve.P256, hashfunc=sha256):
    priv_key = ec.generate_private_key(curve, backend)
    return int_to_hex_str(priv_key.private_numbers().private_value)

def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256, fmt='RAW'):
    if fmt in ['RAW', '04']:
        priv_key = int(priv_key, 16)
        priv_key = ec.derive_private_key(priv_key, curve, backend)
        return point_to_hex_str(priv_key.public_key().public_numbers(), fmt=fmt)
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % fmt)

def gen_keypair(curve=curve.P256, hashfunc=sha256, pub_key_fmt='RAW'):
    priv_key = ec.generate_private_key(curve, backend)
    return int_to_hex_str(priv_key.private_numbers().private_value), \
           point_to_hex_str(priv_key.public_key().public_numbers(),
                            fmt=pub_key_fmt)

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER', 
         sign_size=32):
    if type(data) != bytes:
        data = data.encode()
    priv_key = int(priv_key, 16)
    priv_key = ec.derive_private_key(priv_key, curve, backend)
    if sign_fmt == 'DER':
        return priv_key.sign(data, ec.ECDSA(hashfunc)).hex()
    elif sign_fmt == 'RAW':
        r, s = decode_sig(priv_key.sign(data, ec.ECDSA(hashfunc)))
        return encode_sig(r, s, fmt=sign_fmt, size=sign_size).hex()
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

def verify(pub_key, data, signature, hashfunc=sha256, curve=curve.P256,
           sign_fmt='DER', sign_size=32, pub_key_fmt='RAW'):
    data_bytes = data.encode()
    if pub_key_fmt == 'RAW':
        pub_key_encoded = '04' + pub_key
    elif pub_key_fmt == '04':
        pub_key_encoded = pub_key
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % pub_key_fmt)

    if sign_fmt == 'DER':
        signature = bytes.fromhex(signature)
    elif sign_fmt == 'RAW':
        r, s = decode_sig(bytes.fromhex(signature), fmt="RAW")
        signature = encode_sig(r, s, fmt='DER', size=sign_size)
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

    try:
        pub_key_p = ec.EllipticCurvePublicKey.from_encoded_point(curve, bytes.fromhex(pub_key_encoded)).verify(signature, data_bytes, ec.ECDSA(hashfunc))
        #pub_key_p = ec.EllipticCurvePublicNumbers.from_encoded_point(curve, bytes.fromhex(pub_key_encoded)).public_key(backend).verify(signature, data_bytes, ec.ECDSA(hashfunc))
    except InvalidSignature as e:
        logger.debug("Invalid signature: %s, pub key: %s, data: %s" % (signature, pub_key, data))
        return False
    return True
