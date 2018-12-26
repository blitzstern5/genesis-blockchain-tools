import ctypes 

from . import fill_from_left

ADDRESS_LENGTH = 20
ADDRESS_PART_LEN = 4
ADDRESS_PART_DELIM = '-'

def key_id_to_address(key_id, use_delims=True):
    s = str(ctypes.c_uint64(int(key_id)).value)
    s = fill_from_left(s, exp_len=ADDRESS_LENGTH)
    if use_delims:
        s = ADDRESS_PART_DELIM.join([s[i: i + ADDRESS_PART_LEN] for i in range(0, len(s), ADDRESS_PART_LEN)])
    return s

def address_to_key_id(address):
    return ctypes.c_int64(int(address.replace(ADDRESS_PART_DELIM, '').lstrip('0'))).value

