import os

from setuptools import setup, find_packages

__VERSION__ = '0.3.0'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'pytest',
    'cryptography',
    'crccheck',
    'msgpack-pure',
    'msgpack',
    'puremagic',
]

setup(
    name='genesis_blockchain_tools',
    version=__VERSION__,
    description='Genesis BlockChain Tools',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: Blockchain",
    ],
    author='blitzstern5',
    author_email='blitzstern5@gmail.com',
    url='https://github.com/blitzstern5/genesis-blockchain-tools',
    keywords='crypto blockchain genesis tools',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='genesis_blockchain_tools',
    install_requires=requires,
)
