"""Provision commonly used math tools."""
import numpy as np
import numpy.random as rnd
# import scipy as sp  # useless
from scipy import linalg
from scipy import stats

from scipy.linalg import svd
from scipy.linalg import eig
# eig() of scipy.linalg necessitates using np.real_if_close().
from scipy.linalg import sqrtm, inv, eigh

# Don't shadow builtins: sum, max, abs, round, pow
from numpy import (
    pi, nan,
    floor, ceil,
    sqrt, log, log10, exp, sin, cos, tan,
    mean, prod, diff, cumsum,
    array, asarray, asmatrix,
    linspace, arange, reshape,
    eye, zeros, ones, diag, trace
)

np.set_printoptions(
    precision=6,    # shorten from 8
    threshold=200,  # max total
    suppress=True,  # don't use science notation, coz occurs to much.
                    # NB: array([0.1e-precision]) prints as 0
)
# Just let terminal do wrapping. This is uglier,
# but it's hard to update lw automatically upon term resize. 
np.set_printoptions(linewidth=9999)
