import datetime 
import msgpack
import random
from random import randint

from ..crypto import sign, get_public_key
from ..convert import encode_length_plus_data
from ..crypto.genesis import public_key_to_address, double_hash

from .fields import (
    Field, IntegerField, StringField, BooleanField, MoneyField, FloatField,
    ArrayField, BytesField, FileField,
)

class Error(Exception): pass
class SchemaIsNotSetError(Error): pass
class PublicKeyIsNotSetError(Error): pass
class NonOptionalParamIsNotSetError(Error): pass
class UnknownParamTypeError(Error): pass
class UnknownParamError(Error): pass

class Contract:
    type_field_map = {
        "bool": BooleanField,
        "int": IntegerField,
        "float": FloatField,
        "money": MoneyField,
        "string": StringField,
        "bytes": BytesField,
        "array": ArrayField,
        "file": FileField,
    }
    def update_from_schema(self, schema):
        self.schema = schema
        if 'id' in self.schema:
            self.id = schema['id']
        if 'fields' in self.schema:
            self.fields = schema['fields']
        if self.fields:
            self.fields_names = []
            [self.field_names.append(f['name']) for f in self.fields]

    def check_input_params(self):
        for name in self.params:
            if name not in self.field_names:
                raise UnknownParamError(name)

    def prep_params(self):
        self._params = {}
        for field in self.fields:
            if field['type'] not in self.type_field_map:
                raise UnknownParamTypeError(field['type'])
            if field['name'] in self.params:
                self._params[field['name']] = self.type_field_map[field['type']](self.params[field['name']]).value
            else:
                if not field['optional']:
                    raise NonOptionalParamIsNotSetError(field['name'])

    def get_struct(self):
        d = {
            'Header': {
                'ID': self.id,
                'Time': self.time,
                'Nonce': self.nonce,
                'EcosystemID': self.ecosystem_id,
                'KeyID': self.key_id,
                'NetworkID': self.network_id,
                'PublicKey': self.public_key,
            },
            'Params': self._params
        }
        return d

    def serialize(self):
        return msgpack.packb(self.get_struct(), use_bin_type=True)

    def calc_hash(self):
        return double_hash(self.serialize())

    def sign(self):
        return bytes.fromhex(sign(self.private_key, double_hash(self.serialize())))

    def concat(self):
        return self.tx_header \
                + encode_length_plus_data(self.serialize()) \
                + encode_length_plus_data(self.sign())

    def __init__(self, *args, **kwargs):
        self.schema = kwargs.get('schema', None)
        if not self.schema:
            raise SchemaIsNotSetError(self.schema)
        self.fields = kwargs.get('fields', None)
        self.field_names = []
        self.tx_header = kwargs.get('tx_header', bytes([0x80]))
        self.id = kwargs.get('id', kwargs.get('ID', None))
        self.time = kwargs.get('time',
                               kwargs.get('Time', 
                               int(datetime.datetime.now().timestamp())))
        random.seed()
        self.nonce = kwargs.get('nonce', kwargs.get('Nonce',
                                                 randint(0, 10000000000000)))
        self.update_from_schema(self.schema)
        self.ecosystem_id = kwargs.get('ecosystem_id',
                                       kwargs.get('EcosystemID', 1))
        self.network_id = kwargs.get('network_id',
                                      kwargs.get('NetworkID', 1))
        self.token_ecosystem = kwargs.get('token_ecosystem',
                                          kwargs.get('TokenEcosystem', 0))
        self.signed_by = kwargs.get('signed_by', 
                                    kwargs.get('SignedBy', '0'))
        self.bin_signatures = kwargs.get('bin_signatures',
                                         kwargs.get('BinSignatures', None))
        self.private_key = kwargs.get('private_key', None)
        self.public_key = kwargs.get('public_key',
                    kwargs.get('PublicKey',
                               bytes.fromhex(get_public_key(self.private_key))))
        if not self.public_key:
            PublicKeyIsNotSetError(self.public_key)
        self.key_id = public_key_to_address(self.public_key)
        self.max_sum = kwargs.get('max_sum', kwargs.get('MaxSum', ''))
        self.pay_over = kwargs.get('pay_over', kwargs.get('PayOver', ''))
        self.params = kwargs.get('params', kwargs.get('Params', {}))
        self.check_input_params()
        self.prep_params()

