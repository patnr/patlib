"""Modules from standard lib.
"""

import sys
import os
from pathlib import Path
import json
import time
import re
# import dataclasses as dcs
# from typing import Optional, Any

import builtins
import warnings
import contextlib
import subprocess

# Profiling
try:
    profile = builtins.profile     # will exists if launched via kernprof
except AttributeError:
    def profile(func): return func # provide a pass-through version.


@contextlib.contextmanager
def nonchalance(*exceptions):
    """Like contextlib.suppress(), but ignores (almost) all by default."""
    with contextlib.suppress(exceptions or Exception):
        yield

@contextlib.contextmanager
def suppress_w(warning):
    """Suppress warning messages of class `warning`."""
    warnings.simplefilter("ignore",warning)
    yield
    warnings.simplefilter("default",warning)

# Raise exception on warning
#warnings.filterwarnings('error',category=RuntimeWarning)
#warnings.filterwarnings('error',category=np.VisibleDeprecationWarning)


@contextlib.contextmanager
def rewrite(fname):
    """File-editor contextmanager.

    Example:

    >>> with rewrite("myfile.txt") as lines:
    >>>     for i, line in enumerate(lines):
    >>>         lines[i] = line.replace("old","new")
    """
    with open(fname, 'r') as f:
        lines = [line for line in f]

    yield lines

    with open(fname, 'w') as f:
        f.write("".join(lines))


class Timer():
    """Timer context manager.

    Example::

    >>> with Timer('<description>'):
    >>>     time.sleep(1.23)
    [<description>] Elapsed: 1.23
    """

    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        # pass # Turn off timer messages
        if self.name:
            print('[%s]' % self.name, end=' ')
        print('Elapsed: %s' % (time.time() - self.tstart))


def sub_run(*args, check=True, capture_output=True, text=True, **kwargs):
    """`subprocess.run`, with changed defaults, returning stdout.

    Example:
    >>> gitfiles = sub_run(["git", "ls-tree", "-r", "--name-only", "HEAD"])
    >>> # Alternatively:
    >>> # gitfiles = sub_run("git ls-tree -r --name-only HEAD", shell=True)
    >>> # Only .py files:
    >>> gitfiles = [f for f in gitfiles.split("\n") if f.endswith(".py")]
    """

    x = subprocess.run(*args, **kwargs,
            check=check, capture_output=capture_output, text=text)

    if capture_output:
        return x.stdout



@contextlib.contextmanager
def set_tmp(obj, attr, val):
    """Temporarily set an attribute.

    Example:
    >>> class A:
    >>>     pass
    >>> a = A()
    >>> a.x = 1  # Try deleting this line
    >>> with set_tmp(a,"x","TEMPVAL"):
    >>>     print(a.x)
    >>> print(a.x)

    Based on
    http://code.activestate.com/recipes/577089/
    """

    was_there = False
    tmp = None
    if hasattr(obj, attr):
        try:
            if attr in obj.__dict__:
                was_there = True
        except AttributeError:
            if attr in obj.__slots__:
                was_there = True
        if was_there:
            tmp = getattr(obj, attr)
    setattr(obj, attr, val)

    try:
        yield  # was_there, tmp
    except BaseException:
        raise
    finally:
        if not was_there:
            delattr(obj, attr)
        else:
            setattr(obj, attr, tmp)


# https://stackoverflow.com/a/2669120
def sorted_human(lst):
    """Sort the given iterable in the way that humans expect."""
    def convert(text): return int(text) if text.isdigit() else text
    def alphanum_key(key): return [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(lst, key = alphanum_key)


def find_1st_ind(xx):
    try:
        return next(k for k, x in enumerate(xx) if x)
    except StopIteration:
        return None


def do_once(fun):
    def new(*args, **kwargs):
        if new.already_done:
            return None  # do nothing
        else:
            new.already_done = True
            return fun(*args, **kwargs)
    new.already_done = False
    return new
