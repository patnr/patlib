"""A small, personal, `pylab`.

Its purpose is to provide shorthands,
and so should not be used in production code.
It may be loaded with wildcard, eg:

- from pylib.all import *  # executes all submodules
- from pylib.math import * # won't execute the other submodules
"""

from importlib.metadata import version

try:
    __version__ = version(__name__)
except:
    pass

