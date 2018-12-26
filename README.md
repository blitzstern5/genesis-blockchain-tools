Genesis BlockChain Tools
========================

Setup
-----

## Prerequisites:

Currenty five cryptographic backend modules are supported:
* [cryptography](https://github.com/pyca/cryptography) (default, required)
* [python-ecdsa](https://github.com/warner/python-ecdsa)
* [ECPy](http://ubinity.github.io/ECPy/)
* [fastecdsa](https://github.com/AntonKueltz/fastecdsa)
* [rubenesque](https://github.com/latchset/python-rubenesque)

### Setting up cryptography

It's default and required module. Should be installed automaticaly. But you can install it manually nevertheless:

```
pip install cryptography
```

### Setting up python-ecdsa

python-ecdsa is pure python implementation of ECDSA. It's also the slowest. Use this module if you have issues with dependencies installation (on Windows for exapmle):

```
pip install ecdsa
```

### Setting up ECPy

ECPy is pure python implementation of ECDSA. Use this module if you have issues with dependencies installation (on Windows for exapmle):

```
pip install ECPy
```

### Setting up fastecdsa

fastecdsa is C/C++ module. It's the fastest between others. Use this module if you have no issues with dependencies (on Debian/Ubuntu Linux for example):

```
pip install fastecdsa
```

### Setting up rubenesque

rubenesque is pure python implementaion of ECDSA also. But it's not on PyPI. So if you want to use it you have to install it from github repository directly:

```
pip install git+https://github.com/latchset/python-rubenesque
```

Manual installation:

* Activate your virtualenv
* git clone https://github.com/blitzstern5/genesis-blockchain-tools
* cd genesis-blockchain-tools
* python setup.py install

Using pip:

* Activate your virtualenv
* pip install git+https://github.com/blitzstern5/genesis-blockchain-tools

Using pip/requirements:

* Activate your virtualenv
* Add 'git+https://github.com/blitzstern5/genesis-blockchain-tools' to your requirements.txt
* pip install -r requirements.txt

Usage
-----

### Cryptography 

To get public key by private key:

```
from genesis_blockchain_tools.crypto import get_public_key

priv_key = '2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202'
pub_key = get_public_key(priv_key)
```

To sign message/data:

```
from genesis_blockchain_tools.crypto import sign

priv_key = '2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202'
data = "Some data to sign"
signature = sign(priv_key, data)
```

### Client-side transactions

#### Common client-side transaction

To create client-side transaction data:

```
from genesis_blockchain_tools.contract import Contract

priv_key = '2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202'
# schema that was obtained as a result of the GET /api/v2/contract/EditPage query
schema = {'id': 273, 'state': 1, 'active': False, 'tableid': '13', 'walletid': '-6097185355090423139', 'tokenid': '1', 'address': '1234-9558-7186-1912-8477', 'fields': [{'name': 'Id', 'type': 'int', 'optional': False}, {'name': 'Value', 'type': 'string', 'optional': True}, {'name': 'Menu', 'type': 'string', 'optional':
True}, {'name': 'Conditions', 'type': 'string', 'optional': True}, {'name': 'ValidateCount', 'type': 'int', 'optional': True}, {'name': 'ValidateMode', 'type':
'string', 'optional': True}], 'name': '@1EditPage'} 
contract = Contract(schema=schema, private_key=priv_key, params={'Id': 2, 'Value': 'notifications'})
tx_bin_data = contract.concat()

```

#### Working with files in client-side transaction/contract:

How to attach a local file to contract:

```
contract = Contract(schema=schema, private_key=priv_key, params={'SomeParam': 'SomeValue', 'File': {'Path': path_to_local_file}})

```

Mime type autodetection is on by default.
File path by default is reduced to basename.

To customize mime type or name use it like this:
```
contract = Contract(schema=schema, private_key=priv_key, params={'SomeParam': 'SomeValue', 'File': {'Path': path_to_local_file, 'Name': 'file.txt', 'MimeType': 'image/gif'}})

```
Also simplified path setting is available:
```
contract = Contract(schema=schema, private_key=priv_key, params={'SomeParam': 'SomeValue', 'File': string_path_to_local_file, 'Name': 'file.txt', 'MimeType': 'image/gif'}})

```
And aslo simplified raw bytes setting is available:
```
contract = Contract(schema=schema, private_key=priv_key, params={'SomeParem': 'SomeValue, 'File': bytes_var, 'Name': 'file.txt', 'MimeType': 'image/gif'}})

```

Requirements
------------

Tested on Python 3.x only yet
