import os
import pytest
import tempfile

import puremagic
import re
import base64

from genesis_blockchain_tools.utils import find_mime_type_recursive
from genesis_blockchain_tools.contract.fields import (
    Field, IntegerField, StringField, BooleanField, MoneyField, FloatField,
    ArrayField, BytesField, FileField,
)

def test_field_object():
    f = Field()
    f.value = 3
    assert f.value == 3

    f = Field(4)
    assert f.value == 4

def test_integer_field():
    i = IntegerField()
    i.value = 3
    assert i.value == 3

    i = IntegerField(4)
    assert i.value == 4

def test_string_field():
    s = StringField()
    s.value = 3
    assert s.value == '3'

    s = StringField(4)
    assert s.value == '4'

def test_boolean_field():
    b = BooleanField()
    b.value = 3
    assert b.value == False

    b = BooleanField(4)
    assert b.value == False

def test_money_field():
    m = MoneyField()
    m.value = 3
    assert m.value == '3'

    m = MoneyField(4)
    assert m.value == '4'

def test_float_field():
    f = FloatField()
    f.value = 3
    assert f.value == float(3)

    f = FloatField(4)
    assert f.value == float(4)

def test_array_field():
    a = ArrayField()
    a.value = 3
    assert a.value == tuple(['3'])

    a = ArrayField([8, 4, 1])
    assert a.value == tuple(['8', '4', '1'])

def test_bytes_field():
    b = BytesField()
    b.value = [3]
    assert b.value == bytearray([3])

    b = BytesField()
    b.value ="some string".encode()
    assert b.value == "some string".encode()

def test_file_field():
    tmp_file = tempfile.mktemp()
    tmp_path = str(tmp_file)
    with open(tmp_path, 'w') as f:
        f.write("this is a test")
        f.close()

    gif_content = b'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'
    tmp_gif_file = tempfile.mktemp()
    tmp_gif_path = str(tmp_gif_file)
    with open(tmp_gif_path, 'bw') as f:
        f.write(base64.b64decode(gif_content))
        f.close()
   
    m = puremagic.magic_file(tmp_gif_path)
    assert find_mime_type_recursive(m) == 'image/gif'

    jpg_content = b'/9j/4QlQaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLwA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA1LjYtYzEzOCA3OS4xNTk4MjQsIDIwMTYvMDkvMTQtMDE6MDk6MDEgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiLz4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8P3hwYWNrZXQgZW5kPSJ3Ij8+/+0ALFBob3Rvc2hvcCAzLjAAOEJJTQQlAAAAAAAQ1B2M2Y8AsgTpgAmY7PhCfv/bAIQAAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQICAgICAgICAgICAwMDAwMDAwMDAwEBAQEBAQECAQECAgIBAgIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMD/90ABAAE/+4ADkFkb2JlAGTAAAAAAf/AABEIABwAHgMAEQABEQECEQH/xABfAAEBAQADAAAAAAAAAAAAAAAJCwUDBwgBAQAAAAAAAAAAAAAAAAAAAAAQAAEEAgICAwADAAAAAAAAAAQCAwUGAQcACAkREhMUFSMyEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMAAAERAhEAPwCf/wABDeiGuKFuWJ7B6hkIwsvbmxKpRYXVcmBF1uTNgIoS6sTezJUdy2kAwkIhmDixclSGSgXmAMEN/qYZefXgMnyRkUcrsyYuo0WP1pODa81zEbUpURWwahFRO0q7Wx65YDB63FBgQ8ZI2SMiQJWVwE0kF6aOMeHytlxDig8EcD//0J//AAE+8QEw3E93KqyrDWXZzWO8oERLrbTyXDD9TWxYzGGXnG2nXCHB/rRjOf8ASsZx6zjGcBj+WoEhvvDsaeIYaHXeKnqW6pQw628OpE3q6p4+0dbSlI+t1QuVfHGVfFWcp95zj3kDZ4H/0Z//AAGC8avWe7Q+y9ZdjbWRVI2nEDWt6vUUi2jg7iu8IZGyNRFudGoTbgcvO1Ia2FfmILaLEdQ2KU838kM+1h3X5bOvB+1t7X7b+jWIZGvNR6focPM0i0WyHD3OyPSY78Nwm11MkxyWtcdBHPEYIkR1vYyOE4v2pKUqWAJcD//Sn/8AATjTPaK7Vvr4JZiavr+3WfreLIUrU1guMRNy5sDUthSLzdjr5ArNjBh5OMdatRiG0PCq+KFpTnKsITjAc+wuyNpnutcbsBuo0CBvVvritDn22CjrEzLg6vDVKiE1qI/kLRJAgjS6YlCyf6V+nnXVs4aU5nPAMDgf/9k='
    tmp_jpg_file = tempfile.mktemp()
    tmp_jpg_path = str(tmp_jpg_file)
    with open(tmp_jpg_path, 'bw') as f:
        f.write(base64.b64decode(jpg_content))
        f.close()
   
    m = puremagic.magic_file(tmp_jpg_path)
    assert find_mime_type_recursive(m) == 'image/jpeg'

    png_content = b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAcCAYAAAB2+A+pAAABS2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxMzggNzkuMTU5ODI0LCAyMDE2LzA5LzE0LTAxOjA5OjAxICAgICAgICAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIi8+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgo8P3hwYWNrZXQgZW5kPSJyIj8+IEmuOgAAA09JREFUSIm1lk1LMl0YgK9pdNQZR0FFsxSCMApJidCFRIsI2gW1bdU/eX9F1K7/YCDRJoKgDyQKQhCkRSFTlmN+jV85z6L3fVb14vQ83nAWw5xzXdznvs+cATCtjqmpKTMQCJiAGY/HTZ/PZ5mB1QXBYNDc3983FxYWTMDc29szj4+PLYsnsBibm5s8PDxQKBQAyGazRCIRUqmUJY5lcTgcxu/3k8lkCAQCKIrC0dERKysr4xXXajVEUUSWZba2thAEgXw+jyRJljg2q+JSqYSu67y+vtJqtahWq6yvr3N9fW2JIwL/WFnQaDSQJIlwOMzOzg7D4ZB8Pk+hUKDT6YzMsbzVmqbR6XRYW1vj9vaWVCrF3Nwcuq5b4lgWAwiCgN/v//08MzODKIrjFw8GA1RVRVVVRFHE5XJZZvxIbLfbeX9/p9vt0u12kSTJclf/SNxutxkMBhiGgaZpOBwO3G73+MWdTgdRFFEUhW63S7PZRJblL+cKgvD3xM1mk16vR6vVwjAMVFXF4XB8Odc0zb8n7vV6GIaB1+vF4XAQDAbxeDyWGD/e6kqlgsvlQtd1er0eqqqOX2yz2dA0jVarhdvt5uXlBbvdPn6xJEkMh0PK5TLlchlZlolGo5YYli8J+PyAeL1eJicnmZiYIBAIMBwOLTF+lLEsy8iyTKVSYXFxkWg0Sq1WG7/4+fkZWZbxeDw0Gg2Ab4/TdyHw74/XKLG7u0soFKJWq1GtVpFlGZfLRSwW4+zsDIBut8tgMODk5OR/WSPV2G63s729TSKR4OPjg7m5OXK5HIIgEAqFOD8/x+FwEIlEiMVi2Gw2+v0+p6enfyZOJBKsrq5yeHjI4+Mj8/PzxONxAoEAPp8Pt9tNq9Uim83idDpZWloinU5zdXVFu93+kjlSjVVVxeVyEQ6H0TSNfD6PoihcXFxwcHCAoiiEQiGKxSJ3d3fA50Vis32f10gZ39/fUy6XcTqdJJNJ+v0+kiSRTqdpt9s4nU6KxSKZTAbDMBBFkaenJ+r1+rfMkZtrY2ODRCIBfDaQYRjouo6u6ySTSer1OjabjVAoRKlUIpfL8fb29udigNnZWaanpzFNk8vLS3q93u93y8vLqKpKv9/n5ubm29r+F78AmGZ4Lz2bZYkAAAAASUVORK5CYII='
    tmp_png_file = tempfile.mktemp()
    tmp_png_path = str(tmp_png_file)
    with open(tmp_png_path, 'bw') as f:
        f.write(base64.b64decode(png_content))
        f.close()
   
    m = puremagic.magic_file(tmp_png_path)
    assert find_mime_type_recursive(m) == 'image/png'

    b = FileField()
    b.path = tmp_path
    d = b.to_dict()
    assert len(d) == 3
    assert d['Body'] == b'this is a test'
    assert d['Name'] == os.path.basename(tmp_path)
    assert d['MimeType'] == 'text/plain'

    b = FileField(name='test.txt', path=tmp_path, mime_type='weird/odd')
    d = b.to_dict()
    assert len(d) == 3
    assert d['Name'] == 'test.txt'
    assert d['Body'] == b'this is a test'
    assert d['MimeType'] == 'weird/odd'

    b = FileField(name='test.txt', mime_type='empty/body')
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'test.txt'
    assert d['Body'] == bytes()
    assert d['MimeType'] == 'empty/body'

    b = FileField(path=tmp_path)
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == os.path.basename(tmp_path)
    assert d['Body'] == b'this is a test'
    assert d['MimeType'] == 'text/plain'

    b = FileField(name='some.txt', body=b'custom body')
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'some.txt'
    assert d['Body'] == b'custom body'
    assert d['MimeType'] == 'text/plain'

    b = FileField(name='some.txt', body=b'custom body',
                  mime_type='custom/mime')
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'some.txt'
    assert d['Body'] == b'custom body'
    assert d['MimeType'] == 'custom/mime'

    b = FileField({'name': 'some1.txt', 'body': b'custom1 body',
                   'mime_type': 'custom/mime1'})
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'some1.txt'
    assert d['Body'] == b'custom1 body'
    assert d['MimeType'] == 'custom/mime1'
   
    b = FileField({'Name': 'some2.txt', 'Body': b'custom2 body',
                   'MimeType': 'custom/mime2'})
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'some2.txt'
    assert d['Body'] == b'custom2 body'
    assert d['MimeType'] == 'custom/mime2'

    b = FileField({'path': tmp_path})
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == os.path.basename(tmp_path)
    assert d['Body'] == b'this is a test'
    assert d['MimeType'] == 'text/plain'

    b = FileField({'Path': tmp_gif_path, 'Name': 'file.gif'})
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'file.gif'
    assert d['Body'] == base64.b64decode(gif_content)
    assert d['MimeType'] == 'image/gif'

    b = FileField({'Path': tmp_jpg_path, 'Name': 'file.jpg'})
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'file.jpg'
    assert d['Body'] == base64.b64decode(jpg_content)
    assert d['MimeType'] == 'image/jpeg'

    b = FileField({'path': tmp_png_path, 'Name': 'file.png'})
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'file.png'
    assert d['Body'] == base64.b64decode(png_content)
    assert d['MimeType'] == 'image/png'

    b = FileField({'path': tmp_png_path, 'Name': 'file.png',
                    'MimeType': 'custom/mime'})
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'file.png'
    assert d['Body'] == base64.b64decode(png_content)
    assert d['MimeType'] == 'custom/mime'

    b = FileField(tmp_png_path)
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert len(d['Name']) > 0
    assert d['Body'] == base64.b64decode(png_content)
    assert d['MimeType'] == 'image/png'

    b = FileField(base64.b64decode(gif_content))
    d = b.to_dict()
    d = b.value
    assert len(d) == 3
    assert d['Name'] == 'Filename'
    assert d['Body'] == base64.b64decode(gif_content)
    assert d['MimeType'] == 'image/gif'
