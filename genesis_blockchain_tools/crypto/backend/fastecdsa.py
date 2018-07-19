from fastecdsa import keys, curve, ecdsa
from fastecdsa.point import Point
from hashlib import sha256

from ..formatters import encode_sig, decode_sig
from ...convert import int_to_hex_str
from .errors import (
    UnknownPointFormatError, UnknownPublicKeyFormatError, 
    UnknownSignatureFormatError
)

backend_name = 'fastecdsa'

def split_str_to_halves(s):
    return s[0:len(s)//2], s[len(s)//2 if len(s)%2 == 0 else ((len(s)//2)+1):]

def point_to_hex_str(key, fmt='RAW'):
    hex_str = int_to_hex_str(key.x) + int_to_hex_str(key.y)
    if fmt == 'RAW':
        return hex_str
    elif fmt == '04':
        return '04' + hex_str
    else:
        raise UnknownPointFormatError("fmt: '%s'" % fmt)

def gen_private_key(curve=curve.P256, hashfunc=sha256):
    priv_key = keys.gen_private_key(curve)
    return int_to_hex_str(priv_key)

def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256, fmt='RAW'):
    if fmt in ['RAW', '04']:
        priv_key = int(priv_key, 16)
        pub_key = keys.get_public_key(priv_key, curve=curve)
        return point_to_hex_str(pub_key, fmt=fmt)
    else:
        raise UnknownPointFormatError("fmt: '%s'" % fmt)

def gen_keypair(curve=curve.P256, hashfunc=sha256, pub_key_fmt='RAW'):
    if pub_key_fmt in ['RAW', '04']:
        priv_key = keys.gen_private_key(curve=curve)
        pub_key = keys.get_public_key(priv_key, curve=curve)
        return int_to_hex_str(priv_key), point_to_hex_str(pub_key,
                              fmt=pub_key_fmt)
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % fmt)

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER',
         sign_size=32):
    r, s = ecdsa.sign(data, int(priv_key, 16), hashfunc=hashfunc)
    if sign_fmt in ['RAW', 'DER']:
        return encode_sig(r, s, fmt=sign_fmt, size=sign_size).hex()
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

def verify(pub_key, data, signature, hashfunc=sha256, curve=curve.P256,
           sign_fmt='DER', sign_size=32, pub_key_fmt='RAW'):
    if pub_key_fmt == 'RAW':
        pub_key_encoded = pub_key.encode()
    elif pub_key_fmt == '04':
        pub_key_encoded = pub_key[2:].encode()
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % sign_fmt)
    x, y = split_str_to_halves(pub_key_encoded)
    x, y = int(x, 16), int(y, 16)
    pub_key_point = Point(x, y, curve=curve)

    if sign_fmt in ['RAW', 'DER']:
        r, s = decode_sig(bytes.fromhex(signature), fmt=sign_fmt)
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

    priv_key = keys.gen_private_key(curve)
    valid = ecdsa.verify((r, s), data, pub_key_point, curve=curve,
                         hashfunc=hashfunc)
    return valid

