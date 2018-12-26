import os
import datetime
import re
import logging
import puremagic
from puremagic.main import PureError

from ..utils import find_mime_type_recursive, is_string, is_bytes

logger = logging.getLogger(__name__)

class Field:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __init__(self, *args):
        if len(args) > 0:
            self.value = args[0]

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self)

class IntegerField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = int(value)

class StringField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = str(value)

    def __repr__(self):
        return "'%s'" % str(self.value)


class MoneyField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = str(value).replace(',', '.')

    def __repr__(self):
        return '"%s"' % str(self.value)

class BooleanField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = bool(re.search(r'^\s*(true|yes|1(.(0)+)?)\s*$',
                                     str(value), re.IGNORECASE))

class FloatField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = float(value)

class ArrayField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = tuple(map(lambda v: str(v), value))
        except TypeError:
            self._value = tuple([str(value)])

class BytesField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if is_bytes(value):
            self._value = value
        else:
            try:
                self._value = bytearray(tuple(map(lambda v: int(v), value)))
            except TypeError:
                self._value = bytearray([int(value)])

class FileField(Field):
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        if self._path:
            self._path = str(self._path)
            self.name = os.path.basename(self._path)

    @property
    def name(self):
        if not self._name and not self.path:
            return self.default_name
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self._name:
            self._name = str(self._name)

    @property
    def mime_type(self):
        if self._mime_type:
            return self._mime_type
        else:
            if self.auto_detect_mime_type:
                if self.path and os.path.isfile(self.path) \
                and os.access(self.path, os.R_OK):
                    m = find_mime_type_recursive(
                            puremagic.magic_file(self.path)
                    )
                    if m:
                        return m
                    else:
                        logger.warning("Can't detect mime type of file '%s'. Using default mime type: %s" % (self.path, self.default_mime_type))
                        return self.default_mime_type
                elif not self.path and self.body:
                    try:
                        m = find_mime_type_recursive(
                                puremagic.magic_string(self.body)
                        )
                    except PureError:
                        m = None
                    if m:
                        return m
                    else:
                        logger.warning("Can't detect mime type of body. Using default mime type: %s" % self.default_mime_type)
                        return self.default_mime_type
                else:
                    logger.warning("File '%s' isn't readable. Skipping mime type auto detection, using default mime type: %s" % (self.path, self.default_mime_type))
                    return self.default_mime_type
            else:
                return self.default_mime_type

    @mime_type.setter
    def mime_type(self, value):
        self._mime_type = value
        if self._mime_type:
            self._mime_type = str(value)

    def from_dict(self, d):
        if d.get('path') or d.get('Path'):
            self.path = d.get('path', d.get('Path'))
        if d.get('name') or d.get('Name'):
            self.name = d.get('name', d.get('Name'))
        if d.get('body') or d.get('Body'):
            self.body = d.get('body', d.get('Body'))
        self._did_read = False
        self.file_open_mode = d.get('file_open_mode', 'rb')
        #if 'b' in self.file_open_mode:
        #    self.default_mime_type = d.get('default_mime_type', 'application/octet-stream')
        #else:
        #    self.default_mime_type = d.get('default_mime_type', 'text/plain')
        self.auto_detect_mime_type = d.get('auto_detect_mime_type', True)
        self.default_mime_type = d.get('default_mime_type', 'text/plain')
        self.default_name = d.get('default_name', 'Filename')
        if d.get('mime_type') or d.get('MimeType'):
            self.mime_type = d.get('mime_type', d.get('MimeType'))

    def __init__(self, *args, **kwargs):
        self._name = None
        self._path = None
        self._body = None
        self._mime_type = None
        if len(args) > 0:
            self.value = args[0]
        self.from_dict(kwargs)

    @property
    def body(self):
        return self._body if self._body is not None else bytes()

    @body.setter
    def body(self, value):
        self._body = value

    def read(self):
        with open(self.path, self.file_open_mode) as f:
            self.body = f.read()
            f.close()
            self._did_read = True
        return self.body

    def safe_read(self):
        if not self.path:
            logger.warning("Path isn't set. Skipping readding")
            return
        self.read()

    def to_dict(self):
        if not self._did_read:
            self.safe_read()
        d = {
            'Name': self.name,
            'MimeType': self.mime_type,
            'Body': self.body,
        }
        return d

    @property
    def value(self):
        return self.to_dict()

    @value.setter
    def value(self, value):
        if type(value) == dict:
            self.from_dict(value)
        elif is_string(value):
            self.path = value
        elif type(value) == bytes:
            self.body = value

