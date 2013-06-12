from ethel import __appname__, __version__
from setuptools import setup


long_description = ""

setup(
    name=__appname__,
    version=__version__,
    scripts=[],
    packages=[
        'ethel',
    ],
    author="Paul Tagliamonte",
    author_email="tag@pault.ag",
    long_description=long_description,
    description='Ethyl!',
    license="Expat",
    url="http://deb.io/",
    platforms=['any'],
    entry_points = {
        'console_scripts': [
             'ethel-source = ethel.cli:get_source_package',
             'ethel-binary = ethel.cli:get_binary_package',

             'etheld = ethel.daemon:main',
             'ethel-update = ethel.utils:doupdate',
        ],
    }
)
