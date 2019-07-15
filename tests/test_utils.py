import pytest
import re
from collections import namedtuple

from genesis_blockchain_tools.utils import find_mime_type_recursive

def test_find_mime_type_recursive():
    d = [['.gif', 'image/gif', 'Graphics interchange format file (GIF87a)', 0.4], ['.gif', '', 'GIF file', 0.4]]
    assert find_mime_type_recursive(d) == 'image/gif'

    d = [['.gif', 'image/gif', 'Graphics interchange format file (GIF87a)', 0.4], ['.gif', '', 'GIF file', 0.4]]
    assert find_mime_type_recursive(d) != 'image/png'

    d = {
        'byte_match': 'value1',
        'offset': '123',
        'mime_type': 'image/gif',
        'extension': '.gif',
        'name': 'gif name',
    } 
    NamedTuple = namedtuple('NamedTuple', tuple(d.keys()))
    nt = NamedTuple(**d)
    assert find_mime_type_recursive(nt) == 'image/gif'

    d = {
        'byte_match': 'value1',
        'offset': '123',
        'mime_type': 'image/png',
        'extension': '.png',
        'name': 'png name',
    } 
    NamedTuple = namedtuple('NamedTuple', tuple(d.keys()))
    nt = NamedTuple(**d)
    assert find_mime_type_recursive(nt) != 'image/gif'
