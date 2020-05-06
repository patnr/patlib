"""Various tools
"""

import numpy as np

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



# stackoverflow.com/a/11103301
def on_xlim_changed(ax):
    """
    Autoscale y-axis for subplots with sharex=True.
    
    Usage:
    for ax in fig.axes:
        ax.callbacks.connect('xlim_changed', on_xlim_changed)
    """
    xlim = ax.get_xlim()
    for a in ax.figure.axes:
            # shortcuts: last avoids n**2 behavior when each axis fires event
            if a is ax or len(a.lines) == 0 or getattr(a, 'xlim', None) == xlim:
                    continue

            ylim = np.inf, -np.inf
            for l in a.lines:
                    x, y = l.get_data()
                    # faster, but assumes that x is sorted
                    start, stop = np.searchsorted(x, xlim)
                    yc = y[max(start-1,0):(stop+1)]
                    ylim = min(ylim[0], np.nanmin(yc)), max(ylim[1], np.nanmax(yc))

            # TODO: update limits from Patches, Texts, Collections, ...

            # x axis: emit=False avoids infinite loop
            a.set_xlim(xlim, emit=False)

            # y axis: set dataLim, make sure that autoscale in 'y' is on 
            corners = (xlim[0], ylim[0]), (xlim[1], ylim[1])
            a.dataLim.update_from_data_xy(corners, ignore=True, updatex=False)
            a.autoscale(enable=True, axis='y')
            # cache xlim to mark 'a' as treated
            a.xlim = xlim



# import pyperclip
# def paste_array(dtype=float, sep=" "):
    # """Paste array from clipboard (plaintext) into python.

    # NB: only works on Matlab matrices of size (1,length).
    # But it should be easy to adapt this function for other shapes.

    # In Matlab, to copy into clipboard, use:
    # (Matlab)>>> clipboard('copy',myMatrix)
    # """

    # # Grab from clipboard
    # d = pyperclip.paste()[1:-1]

    # # Detect and trim brackets
    # i0 =    1 if d[ 0]=='[' else None
    # i1 = -1 if d[-1]==']' else None

    # d = np.fromstring(d, dtype=dtype, sep=sep)
    # return d
