import pytest

from genesis_blockchain_tools.convert import *

def test_fill_from_left():
    src = "abc"
    assert len(fill_from_left(src)) == 64
    assert fill_from_left(src) == "0000000000000000000000000000000000000000000000000000000000000abc"

def test_int_to_hex_str():
    assert int_to_hex_str(123456789) == '00000000000000000000000000000000000000000000000000000000075bcd15'
    assert int_to_hex_str(1234) == '00000000000000000000000000000000000000000000000000000000000004d2'

def test_encode_length():
    assert [c for c in encode_length(67)] == [67]
    assert [c for c in encode_length(300)] == [130, 1, 44]
    assert [c for c in encode_length(1024)] == [130, 4, 0]
    assert [c for c in encode_length(1000000)] == [131, 15, 66, 64]
    assert [c for c in encode_length(2000000)] == [131, 30, 132, 128]
    assert [c for c in encode_length(2348278648854754)] == [135, 8, 87, 191, 58, 178, 216, 226]
    assert [c for c in encode_length(-44754)] == [136, 255, 255, 255, 255, 255, 255, 81, 46]
    not_int64_error_caught = False
    try:
        encode_length(2**64)
    except NotInt64Error:
        not_int64_error_caught = True
    assert not_int64_error_caught

    not_int64_error_caught = False
    try:
        encode_length(-2**64)
    except NotInt64Error:
        not_int64_error_caught = True
    assert not_int64_error_caught

def test_encode_length_plus_data():
    assert [c for c in encode_length_plus_data("some string".encode())] == [11, 115, 111, 109, 101, 32, 115, 116, 114, 105, 110, 103]
    assert [c for c in encode_length_plus_data("what a boring shit".encode())] == [18, 119, 104, 97, 116, 32, 97, 32, 98, 111, 114, 105, 110, 103, 32, 115, 104, 105, 116,]
    assert [c for c in encode_length_plus_data("this one too".encode())] == [12, 116, 104, 105, 115, 32, 111, 110, 101, 32, 116, 111, 111]
    assert [c for c in encode_length_plus_data("k, enough".encode())] == [9, 107, 44, 32, 101, 110, 111, 117, 103, 104]
    assert [c for c in encode_length_plus_data("pure string")] == [11, 112, 117, 114, 101, 32, 115, 116, 114, 105, 110, 103]
    assert [c for c in encode_length_plus_data(34523)] == [5, 51, 52, 53, 50, 51]
    assert [c for c in encode_length_plus_data(-888345454)] == [10, 45, 56, 56, 56, 51, 52, 53, 52, 53, 52]
