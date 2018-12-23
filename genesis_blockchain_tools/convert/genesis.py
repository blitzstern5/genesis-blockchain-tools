import ctypes 

from . import fill_from_left

ADDRESS_LENGTH = 20

def address_to_wallet(address, use_delims=True):
    s = str(int(address) & 0xffffffffffffffff)
    s = fill_from_left(s, exp_len=ADDRESS_LENGTH)
    if use_delims:
        s = '-'.join((s[0:4], s[4:8], s[8:12], s[12:16], s[16:20]))
    return s

key_id_to_wallet = address_to_wallet

def wallet_to_address(wallet):
    return ctypes.c_int64(int(wallet.replace('-', '').lstrip('0'))).value

wallet_to_key_id = wallet_to_address
