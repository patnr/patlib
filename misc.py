"""Various tools
"""

import numpy as np

# TODO: include Bunch and NestedPrint?
# TODO: implement sort_keys choice

def aprint(A):
    """
    Array summary.

    TODO: Adjust edgeitems depending on int/float.
    """
    shape = A.shape
    opts  = np.get_printoptions()

    #lw = get_lw(do_compensate_prompt=False)
    #if len(shape)==1:
        #nitems = int((lw - 5)/(opts['precision'] + 1)) - 1
        #np.set_printoptions(linewidth=lw,edgeitems=3,threshold=nitems)

    mina = np.abs(A).min()
    maxa = np.abs(A).max()

    print_bold = lambda s: print('\033[94m', s, "\033[0m")

    # Common exponent
    p = opts['precision']
    expo = 1
    if maxa != 0:
        if mina > 10**(p-3):
            expo = int(np.log10(mina))
        elif maxa < 10**-(p-3):
            expo = int(np.log10(maxa))-1

    print_bold("array(")
    if expo==1:
        print(str(A))
        print_bold(")")
    else:
        print(str(A / 10**expo))
        print_bold(") * 1e" + str(expo))

    # Stats
    print("shape             : ", shape)
    print("sparsity          :  {:d}/{:d}".format(A.size-np.count_nonzero(A),A.size))
    print("mean              :  {:11g}"                .format(A.mean()))
    print("std               :  {:11g}"                .format(A.std(ddof=1)))
    print("min, max          :  {:11g}, {:11g}".format(A.min(), A.max()))
    print("min(abs), max(abs):  {:11g}, {:11g}".format(mina, maxa))


import pyperclip
def paste_array(dtype=float, sep=" "):
    """Paste array from clipboard (plaintext) into python.

    NB: only works on Matlab matrices of size (1,length).
    But it should be easy to adapt this function for other shapes.

    In Matlab, to copy into clipboard, use:
    (Matlab)>>> clipboard('copy',myMatrix)
    """

    # Grab from clipboard
    d = pyperclip.paste()[1:-1]

    # Detect and trim brackets
    i0 =  1 if d[ 0]=='[' else None
    i1 = -1 if d[-1]==']' else None

    d = np.fromstring(d, dtype=dtype, sep=sep)
    return d


import json
class JsonDict(dict):
    """Provide json pretty-printing"""
    def __str__(self): return repr(self)
    def __repr__(self):
        s = json.dumps(self, indent=4, sort_keys=False, default=str)
        crop = lambda t: t[:80] + ("" if len(t)<80 else "...")
        s = "\n".join([crop(ln) for ln in s.split("\n")])
        return s


import time
class Timer():
    """Timer.

    Example::

      with Timer('<description>'):
        do_stuff()
    """
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        #pass # Turn off timer messages
        if self.name:
            print('[%s]' % self.name, end='')
        print('Elapsed: %s' % (time.time() - self.tstart))

