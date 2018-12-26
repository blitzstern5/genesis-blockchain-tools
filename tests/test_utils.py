import pytest
import re

from genesis_blockchain_tools.utils import find_mime_type_recursive

def test_find_mime_type_recursive():
    d = [['.gif', 'image/gif', 'Graphics interchange format file (GIF87a)', 0.4], ['.gif', '', 'GIF file', 0.4]]
    assert find_mime_type_recursive(d) == 'image/gif'
