from rubenesque.codecs.sec import encode, decode
from rubenesque.signatures import ecdsa
import rubenesque.curves
from hashlib import sha256

from ..formatters import encode_sig, decode_sig
from ...convert import int_to_hex_str
from .common import point_to_hex_str, split_str_to_halves
from .errors import (
    UnknownPointFormatError, UnknownSignatureFormatError,
    UnknownPublicKeyFormatError
)

backend_name = 'rubenesque'

class CurveByAttrName:
    @property
    def P256(self):
        return rubenesque.curves.find('secp256r1')

curve = CurveByAttrName()

def gen_private_key(curve=curve.P256, hashfunc=sha256):
    priv_key = curve.private_key()
    return int_to_hex_str(priv_key)

def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256, fmt='RAW'):
    if fmt in ['RAW', '04']:
        priv_key = int(priv_key, 16)
        pub_key_obj = curve.generator() * priv_key
        return point_to_hex_str(pub_key_obj, fmt=fmt)
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % fmt)

def gen_keypair(curve=curve.P256, hashfunc=sha256, pub_key_fmt='RAW'):
    priv_key = gen_private_key(curve=curve, hashfunc=hashfunc)
    pub_key = get_public_key(priv_key, curve=curve, hashfunc=hashfunc,
                             fmt=pub_key_fmt)
    return priv_key, pub_key

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER', 
         sign_size=32):
    if type(data) != bytes:
        data = data.decode()
    h = hashfunc(data).digest()
    r, s = ecdsa.sign(curve, int(priv_key, 16), h)
    if sign_fmt in ['DER', 'RAW']:
        return encode_sig(r, s, fmt=sign_fmt, size=sign_size).hex()
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

def verify(pub_key, data, signature, hashfunc=sha256, curve=curve.P256,
           sign_fmt='DER', sign_size=32, pub_key_fmt='RAW'):
    if pub_key_fmt == 'RAW':
        pub_key_encoded = pub_key
    elif pub_key_fmt == '04':
        pub_key_encoded = pub_key[2:]
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % pub_key_fmt)
    x, y = split_str_to_halves(pub_key_encoded)
    x, y = int(x, 16), int(y, 16)
    pub_key_point = curve(x, y)

    if sign_fmt in ['DER', 'RAW']:
        r, s = decode_sig(bytes.fromhex(signature), fmt=sign_fmt)
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

    data_bytes = data.encode()
    h = hashfunc(data_bytes).digest()
    return ecdsa.verify(pub_key_point, h, r, s)

