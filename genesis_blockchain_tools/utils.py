import six
import re

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_string(s):
    return isinstance(s, six.string_types)

def is_bytes(s):
    return type(s) == bytes

def find_mime_type_recursive(m):
    if m and type(m) == list:
        for item in m:
            found = find_mime_type_recursive(item)
            if found:
                return found
    elif is_string(m) and re.search(r'\w+\/\w+', m, re.IGNORECASE):
        return m 
    elif isinstance(m, object) and hasattr(m, 'mime_type'):
        return m.mime_type
