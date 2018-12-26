import struct

from ..utils import is_number, is_string, is_bytes

class Error(Exception): pass
class NotInt64Error(Error): pass
class UnknownDataTypeError(Error): pass

def fill_from_left(src, exp_len=64, filler='0'):
    return filler * (exp_len - len(src)) + src

def int_to_hex_str(value, exp_len=64):
    return fill_from_left(format(value, 'x'), exp_len=exp_len, filler='0')

def encode_length(length):
    if length < -2**63 or length > 2**63 - 1:
        raise NotInt64Error(length)
    if length >= 0 and length <= 127:
        return struct.pack("B", length)
    buf = bytes(1) + struct.pack(">q", length)
    i = 1
    while buf[i] == 0 and i < 8:
        i += 1
    h = struct.pack("B", 0x80 | 9 - i)
    return h + buf[i:]

def encode_length_plus_data(data):
    if is_string(data):
        data = data.encode()
    elif is_number(data) and not is_bytes(data):
        data = str(data).encode()
    elif is_bytes(data):
        pass
    else:
        raise UnknownDataTypeError()
    return encode_length(len(data)) + data


