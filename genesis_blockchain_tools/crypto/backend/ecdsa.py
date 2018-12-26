from ecdsa import SigningKey, VerifyingKey, NIST256p
from ecdsa.keys import BadSignatureError
from ecdsa.util import sigencode_der

from hashlib import sha256

from ..formatters import encode_sig, decode_sig
from ...convert import int_to_hex_str
from .errors import (
    UnknownPointFormatError, UnknownSignatureFormatError,
    UnknownPublicKeyFormatError
)

backend_name = 'ecdsa'

class CurveByAttrName:
    @property
    def P256(self):
        return NIST256p

curve = CurveByAttrName()

def gen_private_key(curve=curve.P256, hashfunc=sha256):
    priv_key =  SigningKey.generate(curve=curve, hashfunc=hashfunc)
    return priv_key.to_string().hex()

def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256, fmt='RAW'):
    if fmt in ['RAW', '04']:
        priv_key = bytes.fromhex(priv_key)
        priv_key = SigningKey.from_string(priv_key, curve=curve, hashfunc=hashfunc)
        pub_key = priv_key.get_verifying_key().to_string().hex()
        if fmt == '04':
            pub_key = '04' + pub_key
        return pub_key
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % fmt)

def gen_keypair(curve=curve.P256, hashfunc=sha256, pub_key_fmt='RAW'):
    if pub_key_fmt in ['RAW', '04']:
        priv_key =  SigningKey.generate(curve=curve, hashfunc=hashfunc)
        pub_key = priv_key.get_verifying_key().to_string().hex()
        if pub_key_fmt == '04':
            pub_key = '04' + pub_key
        return priv_key.to_string().hex(), pub_key
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % fmt)

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER', 
         sign_size=32):
    if type(data) != bytes:
        data = data.encode()
    priv_key = bytes.fromhex(priv_key)
    priv_key = SigningKey.from_string(priv_key, curve=curve, hashfunc=hashfunc)
    if sign_fmt == "DER":
        return priv_key.sign(data, hashfunc=hashfunc, sigencode=sigencode_der).hex()
    elif sign_fmt == 'RAW':
        return priv_key.sign(data, hashfunc=hashfunc).hex()
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

def verify(pub_key, data, signature, hashfunc=sha256, curve=curve.P256,
           sign_fmt='DER', sign_size=32, pub_key_fmt='RAW'):
    data_bytes = data.encode()

    if pub_key_fmt == 'RAW':
        pub_key_encoded = pub_key
    elif pub_key_fmt == '04':
        pub_key_encoded = pub_key[2:]
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % pub_key_fmt)

    if sign_fmt in ['RAW', 'DER']:
        r, s = decode_sig(bytes.fromhex(signature), fmt=sign_fmt)
        signature = encode_sig(r, s, fmt='RAW', size=sign_size)
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

    vk = VerifyingKey.from_string(bytes.fromhex(pub_key_encoded), curve=curve,
                                  hashfunc=hashfunc)
    try:
        vk.verify(signature, data_bytes)
        return True
    except BadSignatureError:
        return False
