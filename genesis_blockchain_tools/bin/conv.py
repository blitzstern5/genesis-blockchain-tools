import sys
import os
import argparse
from os.path import dirname, abspath

from genesis_blockchain_tools.convert.genesis import (
    key_id_to_address, address_to_key_id
)
from genesis_blockchain_tools.crypto import (
    gen_private_key, get_public_key, gen_keypair, sign,
)
from genesis_blockchain_tools.crypto.genesis import (
    public_key_to_key_id
)

def main(argv=None):
    try:
        if __name__ != '__main__':  # pragma: no cover
            sys.modules['__main__'] = sys.modules[__name__]

        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--fmt')
        parser.add_argument('-k', '--key-id', type=int)
        parser.add_argument('-a', '--address')
        parser.add_argument('-s', '--private-key')
        parser.add_argument('-p', '--public-key')
        
        args = parser.parse_args()
        
        if args.key_id:
            print(key_id_to_address(args.key_id))
        elif args.address:
            print(address_to_key_id(args.address))
        elif args.public_key:
            if args.fmt:
                fmt = args.fmt
            else:
                fmt = '04'
            if len(args.public_key) == 130 and args.public_key[0:2] == '04':
                public_key = args.public_key[2:]
            else:
                public_key = args.public_key
            public_key = bytes.fromhex(public_key)
            key_id = public_key_to_key_id(public_key)
            address = key_id_to_address(key_id)
            print("Key ID: %s " % key_id)
            print("Address: %s " % address)
        elif args.private_key:
            if args.fmt:
                fmt = args.fmt
            else:
                fmt = '04'
            public_key = get_public_key(args.private_key, fmt=fmt)
            public_key_b = bytes.fromhex(public_key)
            key_id = public_key_to_key_id(public_key_b)
            address = key_id_to_address(key_id)
            print("Key ID: %s" % key_id)
            print("Address: %s" % address)
            print("Public Key: %s" % public_key)
        else:
            parser.print_help(sys.stderr)
            sys.exit(0)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':          # pragma: no cover
    main()
