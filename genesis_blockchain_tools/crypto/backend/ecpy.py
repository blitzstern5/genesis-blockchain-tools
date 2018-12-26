from hashlib import sha256
from binascii import a2b_base64, hexlify
from os import urandom

from ecpy.curves import Curve, Point
from ecpy.keys import ECPublicKey, ECPrivateKey
from ecpy.ecdsa import ECDSA

from ..formatters import encode_sig, decode_sig
from ...convert import int_to_hex_str
from .common import point_to_hex_str, split_str_to_halves
from .errors import (
    UnknownPointFormatError, UnknownSignatureFormatError,
    UnknownPublicKeyFormatError
)


backend_name = 'ecpy'

class CurveByAttrName:
    @property
    def P256(self):
        return Curve.get_curve('secp256r1')

curve = CurveByAttrName()

class ECDSAWithSize(ECDSA):
    def __init__(self, *args, **kwargs):
        size = kwargs.pop('size', 64)
        super(ECDSAWithSize, self).__init__(*args, **kwargs)
        self.size = size

    def _do_sign(self, msg, pv_key, k, canonical=False):
        if (pv_key.curve == None):
            raise ECPyException('private key haz no curve')
        curve = pv_key.curve
        n = curve.order
        G = curve.generator
        k = k%n

        msg = int.from_bytes(msg, 'big')
        
        Q = G*k
        kinv = pow(k,n-2,n)
        r = Q.x % n
        if r == 0:
            return None

        s = (kinv*(msg+pv_key.d*r)) %n
        if s == 0:
            return None

        if canonical and (s > (n//2)):
            s = n-s
        
        sig = encode_sig(r, s, fmt=self.fmt, size=self.size)
        
        return sig

def _gen_private_key(curve):
    """Generate a private key to sign data with.

    The private key :math:`d` is an integer generated via a cryptographically secure random number
    generator that lies in the range :math:`[1,n)`, where :math:`n` is the curve order. The specific
    random number generator used is /dev/urandom.

    Args:
        curve: The curve over which the key will be calulated.

    Returns:
        long: Returns a positive integer smaller than the curve order.
    """
    order_bits = 0
    order = curve.order

    while order > 0:
        order >>= 1
        order_bits += 1

    order_bytes = (order_bits + 7) // 8  # urandom only takes bytes
    extra_bits = order_bytes * 8 - order_bits  # bits to shave off after getting bytes

    rand = int(hexlify(urandom(order_bytes)), 16)
    rand >>= extra_bits

    # no modding by group order or we'll introduce biases
    while rand >= curve.order:
        rand = int(hexlify(urandom(order_bytes)), 16)
        rand >>= extra_bits

    return rand

def gen_private_key(curve=curve.P256):
    priv_key = _gen_private_key(curve)
    return int_to_hex_str(priv_key)

def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256, fmt='RAW'):
    if fmt in ['RAW', '04']:
        priv_key = int(priv_key, 16)
        pub_key_obj = ECPrivateKey(priv_key, curve).get_public_key()
        return point_to_hex_str(pub_key_obj.W, fmt=fmt)
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % fmt)

def gen_keypair(curve=curve.P256, hashfunc=sha256, pub_key_fmt='RAW'):
    if pub_key_fmt in ['RAW', '04']:
        priv_key = _gen_private_key(curve)
        pub_key_obj = ECPrivateKey(priv_key, curve).get_public_key()
        return int_to_hex_str(priv_key), point_to_hex_str(pub_key_obj.W, 
                                                          fmt=pub_key_fmt)
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % fmt)

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER', 
         sign_size=32):
    priv_key_int = int(priv_key, 16)
    priv_key_obj = ECPrivateKey(priv_key_int, curve)
    if sign_fmt in ['RAW', 'DER']:
        pass
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)
    signer = ECDSAWithSize(fmt=sign_fmt, size=sign_size)
    if type(data) != bytes:
        data = data.encode()
    msg = hashfunc(data).digest()
    signature = signer.sign(msg, priv_key_obj).hex()
    return signature

def verify(pub_key, data, signature, hashfunc=sha256, curve=curve.P256,
           sign_fmt='DER', sign_size=32, pub_key_fmt='RAW'):
    if sign_fmt in ['RAW', 'DER']:
        pass
    else:
        raise UnknownSignatureFormatError("fmt: '%s'" % sign_fmt)

    if pub_key_fmt == 'RAW':
        pub_key_encoded = pub_key
    elif pub_key_fmt == '04':
        pub_key_encoded = pub_key[2:]
    else:
        raise UnknownPublicKeyFormatError("fmt: '%s'" % pub_key_fmt)
    x, y = split_str_to_halves(pub_key_encoded)
    x, y = int(x, 16), int(y, 16)
    pub_key_point = ECPublicKey(Point(x, y, curve))

    signature = bytes.fromhex(signature)
    signer = ECDSAWithSize(fmt=sign_fmt, size=sign_size)
    msg = hashfunc(data.encode()).digest()
    return signer.verify(msg, signature, pub_key_point)

