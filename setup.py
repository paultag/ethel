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
#            'ethel-buildd = ethel.client:buildd',
#            'ethel-next = ethel.cli:next',
#            'etheld = ethel.daemon:daemon',
#            'ethel-close = ethel.cli:close',
#            'ethel-submit = ethel.cli:submit',
#            'ethel-dget-url = ethel.cli:dget',
#            'ethel-update = ethel.chroot:run_update',
#            'ethel-sbuild = ethel.commands.sbuild:main',
#            'ethel-adequate = ethel.commands.adequate:main',
#            'ethel-piuparts = ethel.commands.piuparts:main',
        ],
    }
)
