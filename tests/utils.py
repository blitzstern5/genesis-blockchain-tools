import string
import random
import json
import os

def gen_rand_str(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_rand_pub_key_fmt():
    fmts = (None, 'RAW', '04')
    return random.choice(fmts)

def get_rand_sign_fmt():
    fmts = (None, 'RAW', 'DER')
    return random.choice(fmts)

def load_fixture_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'fixture', 'data.json')
    with open(path) as f:
        return json.load(f)
