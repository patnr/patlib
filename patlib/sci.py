"""Tools depending on numpy."""

import numpy as np


def uniquish(a, rtol=1e-05, atol=1e-08):
    """Return unique elements of a.

    The ordering is kept, in the sense that
    the earliest appearance of an element is kept.

    Useful for example to eliminate equal roots (up to convergence)
    from `scipy.optimize.fsolve`.

    [Ref1](https://stackoverflow.com/a/37847116)
    [Ref2](https://stackoverflow.com/a/38653131)

    Examples:
    >>> uniquish([1, 2, 3, 1+1e-5])
    array([1., 2., 3.])
    >>> uniquish([1, 2, 3, 1+2e-5])
    array([1., 2., 3., 1.])
    """
    a = np.asarray(a)
    assert a.ndim == 1, "Unique only makes sense for 1d arrays."
    # NB: column vector (e.g.) yields wrong answer.
    equal = np.isclose(a, a[:, None], rtol, atol, equal_nan=True)
    return a[~(np.triu(equal, 1)).any(0)]


def aprint(A):
    """
    Array summary.

    TODO: Adjust edgeitems depending on int/float.
    """
    shape = A.shape
    opts  = np.get_printoptions()  # noqa

    # lw = get_lw(do_compensate_prompt=False)
    # if len(shape)==1:
    #     nitems = int((lw - 5)/(opts['precision'] + 1)) - 1
    #     np.set_printoptions(linewidth=lw,edgeitems=3,threshold=nitems)

    AA = np.abs(A)
    mina = AA.min()
    maxa = AA.max()

    print_bold = lambda s: print('\033[94m', s, "\033[0m")  # noqa

    # Common exponent
    p = opts['precision']
    expo = 1
    if maxa != 0:
        if mina > 10**(p - 3):
            expo = int(np.log10(mina))
        elif maxa < 10**-(p - 3):
            expo = int(np.log10(maxa)) - 1

    print_bold("array(")
    if expo == 1:
        print(str(A))
        print_bold(")")
    else:
        print(str(A / 10**expo))
        print_bold(") * 1e" + str(expo))

    #
    ind2sub = lambda ind: np.unravel_index(ind, A.shape)  # noqa
    min_sub  = ind2sub(np.argmin(A))  # noqa
    max_sub  = ind2sub(np.argmax(A))  # noqa
    amin_sub = ind2sub(np.argmin(AA))
    amax_sub = ind2sub(np.argmax(AA))
    mins = A[min_sub], min_sub, A[amin_sub], amin_sub
    maxs = A[max_sub], max_sub, A[amax_sub], amax_sub

    # Stats
    print("shape    :", shape)
    print("sparsity : {:d}/{:d}".format(A.size - np.count_nonzero(A), A.size))
    print("mean     : {: 10.4g}".format(A.mean()))
    print("std      : {: 10.4g}".format(A.std(ddof=1)))
    print("min (ij) : {: 10.4g} {!r:7},   amin (ij): {: 10.4g} {!r:7}".format(*mins))
    print("max (ij) : {: 10.4g} {!r:7},   amax (ij): {: 10.4g} {!r:7}".format(*maxs))
