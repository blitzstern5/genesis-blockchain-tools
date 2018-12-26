import pytest
import msgpack

from genesis_blockchain_tools.crypto import get_public_key
from genesis_blockchain_tools.contract import (
    Contract,
    Field, IntegerField, StringField, BooleanField, MoneyField, FloatField,
    ArrayField, BytesField, FileField,
    UnknownParamError,
)
from genesis_blockchain_tools.utils import is_number, is_string, is_bytes

def test_contract_1():
    priv_key = 'a5870fbc55861c6e02012be5bb9695be0074d0064022e6be7b28d1f834bba963'
    s = {'id': 261, 'state': 1, 'active': False, 'tableid': '1', 'walletid': '-6097185355090423139', 'tokenid': '1', 'address': '1234-9558-7186-1912-8477', 'fields': [], 'name': '@1MainCondition'}
    c = Contract(schema=s, private_key=priv_key)
    assert c.id == s['id']
    assert c.fields == s['fields']
    assert c.public_key == bytes.fromhex(get_public_key(priv_key))
    s = c.get_struct()
    assert 'Header' in s
    assert s['Header']
    assert type(s['Header']) == dict

    for k in ('ID', 'Time', 'Nonce', 'EcosystemID', 'KeyID', 'NetworkID'):
        assert k in s['Header']
        assert s['Header'][k]
        assert is_number(s['Header'][k])

    for k in ('PublicKey',):
        assert k in s['Header']
        assert s['Header'][k]
        assert is_bytes(s['Header'][k])

    assert 'Params' in s

def test_priv_pub_keys():
    priv_key = 'a5870fbc55861c6e02012be5bb9695be0074d0064022e6be7b28d1f834bba963'
    assert get_public_key(priv_key)

def test_contract_2():
    priv_key = 'a5870fbc55861c6e02012be5bb9695be0074d0064022e6be7b28d1f834bba963'
    s = {'id': 273, 'state': 1, 'active': False, 'tableid': '13', 'walletid': '-6097185355090423139', 'tokenid': '1', 'address': '1234-9558-7186-1912-8477', 'fields': [{'name': 'Id', 'type': 'int', 'optional': False}, {'name': 'Value', 'type': 'string', 'optional': True}, {'name': 'Menu', 'type': 'string', 'optional': True}, {'name': 'Conditions', 'type': 'string', 'optional': True}, {'name': 'ValidateCount', 'type': 'int', 'optional': True}, {'name': 'ValidateMode', 'type': 'string', 'optional': True}], 'name': '@1EditPage'}
    c = Contract(schema=s, private_key=priv_key,
            params={'Id': 2, 'Value': 'notifications'})
    assert c.id == s['id']
    assert c.fields == s['fields']
    assert c.public_key == bytes.fromhex(get_public_key(priv_key))

    unknown_param_error_caught = False
    try:
        c = Contract(schema=s, private_key=priv_key,
                params={'Id': 2, 'Value': 'notifications', 'Some': 'shit'})
    except UnknownParamError:
        unknown_param_error_caught = True
    assert unknown_param_error_caught


    c = Contract(schema=s, private_key=priv_key,
            params={'Id': 2, 'Value': 'notifications'})
    assert c.public_key == bytes.fromhex(get_public_key(priv_key))
    assert type(c.get_struct()) == dict
    assert type(c.serialize()) == bytes
    assert msgpack.unpackb(c.serialize(), raw=False)
    assert type(c.calc_hash()) == bytes
    assert type(c.sign()) == bytes
    assert type(c.concat()) == bytes

