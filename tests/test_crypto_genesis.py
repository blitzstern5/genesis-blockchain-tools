import pytest

from genesis_blockchain_tools.convert.genesis import (
    key_id_to_address, address_to_key_id
)

from genesis_blockchain_tools.crypto import (
    gen_private_key, get_public_key, gen_keypair,
)

from genesis_blockchain_tools.crypto.genesis import (
    checksum, public_key_to_address, public_key_to_key_id, double_hash
)

from .utils import load_fixture_data


FIXTURE_DATA = load_fixture_data()


def test_checksum():
    assert checksum("some string".encode()) == 9
    assert checksum("another string".encode()) == 2
    assert checksum("jeez, it's so boring".encode()) == 0
    assert checksum("and final one".encode()) == 7
    assert checksum("#34423".encode()) == 1

def test_public_key_to_key_id():
    priv_key = gen_private_key()
    fns = (public_key_to_key_id,)
    for i in range(0, len(fns)):
        assert fns[0]("some string".encode()) == 6973694608268913209
        assert fns[0]("another string".encode()) == 826786831444702840
        assert fns[0]("jeez, it's so boring".encode()) == -1106672694297211255
        assert fns[0]("and final one".encode()) == -5961772402273559210
        assert fns[0]("#34423".encode()) == 6729523148133476469 

    for rec in FIXTURE_DATA:
        key_id = rec[0]
        public_key = rec[2]
        assert fns[0](bytes.fromhex(public_key)) == key_id

def test_public_key_address():
    fns = (public_key_to_address,)
    for rec in FIXTURE_DATA:
        address = rec[1]
        public_key = rec[2]
        assert fns[0](bytes.fromhex(public_key)) == address

def test_double_hash():
    assert double_hash("some string".encode()) == bytearray([190, 71, 146, 194, 68, 74, 231, 230, 180, 206, 236, 27, 236, 231, 72, 142, 255, 142, 193, 16, 191, 23, 17, 134, 130, 233, 238, 189, 116, 61, 77, 16])

