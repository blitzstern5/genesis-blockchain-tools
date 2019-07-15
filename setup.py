import os

from setuptools import setup, find_packages

__VERSION__ = '0.3.1'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    name='genesis_blockchain_tools',
    version=__VERSION__,
    description='Genesis BlockChain Tools',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: Blockchain",
    ],
    author='blitzstern5',
    license='MIT',
    author_email='blitzstern5@gmail.com',
    url='https://github.com/blitzstern5/genesis-blockchain-tools',
    keywords='crypto blockchain genesis tools',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3',
    setup_requires=['pytest-runner'],
    install_requires=[
        'cryptography == 2.7',
        'crccheck == 0.6',
        'msgpack-pure == 0.1.3',
        'msgpack == 0.6.1',
        'puremagic == 1.5',
    ],
    tests_require=["pytest >= 5.0.1"],
    extras_require={
        'testing': ["pytest >= 5.0.1"],
    },
    entry_points={
        'console_scripts': [
            'genbc-conv = genesis_blockchain_tools.bin.conv:main',
        ],
    },
)
