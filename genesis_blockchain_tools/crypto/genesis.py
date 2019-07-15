from hashlib import sha256, sha512
from crccheck.crc import Crc64Xz
from ..convert import fill_from_left
from ..convert.genesis import ADDRESS_LENGTH, key_id_to_address

def checksum(data):
    first = 0
    second = 0
    checksum = 0
    for i in range(0, len(data)):
        ch = data[i] - '0'.encode()[0]
        if ch < 0:
            ch += 2**8
        if i & 1:
            first += ch
        else:
            second += ch
    checksum = (second + 3 * first) % 10
    if checksum > 0:
        checksum = 10 - checksum
    return checksum

def public_key_to_key_id(pub_key):
    h256 = sha256(pub_key).digest()
    h512 = sha512(h256).digest()
    crc = Crc64Xz().calc(h512)
    bval = fill_from_left(str(crc), exp_len=ADDRESS_LENGTH, filler='0').encode()
    cs = int(checksum(bval[:len(bval)-1])) & 0xffffffffffffffff
    final = crc - (crc % 10) + cs
    if final > 2**63 - 1:
        final = final - 2**64
    return final

def public_key_to_address(pub_key):
    return key_id_to_address(public_key_to_key_id(pub_key))

def double_hash(data):
    h256 = sha256(data).digest()
    return sha256(h256).digest()
