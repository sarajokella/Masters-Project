#!/usr/bin/env python
#
# little examle using minuit to calculate the mean of a bunch of measurements
import sys
import math
import ctypes
import ROOT

def fcn(npar, grad, retVal, par, flag):
    """
    A little demo function for Minuit to minimise.

    parameters:
    npar    number of parameters passed by Minuit
    grad    array to return gradient in (if supported)
    retVal  value of function to minimise
    par     array of model parameters
    flag    set by minuit depending on what it's calculating

    Technical remark: Since PyROOT adapts this to the C++/FORTRAN interface
    that's expected by MINUIT, all but the last of these parameters actually
    appear to be array-like to python.
    """
    if 2 == flag:  # check if Minuit wants us to calculate gradient
        # indicate that that's not supported at the moment
        for i in xrange(0, npar[0]):
            grad[i] = float('NaN')
    # calculate the chi^2 sum over the data
    chi2sum = 0.
    for i in xrange(0, len(data)):  # loop over data
        tmp = (data[i] - par[0])
        chi2sum = chi2sum + tmp * icovs[i] * tmp
    # return - log LH
    retVal[0] = chi2sum


# create a minimiser for 1 parameter
minuit = ROOT.TMinuit(1)
minuit.Command("SET PRINTOUT 1")  # tell it to be verbose...
minuit.Command("SET WARNINGS")    # and to emit warnings...
minuit.Command("SET STRATEGY 2")  # and to spend time to get good errors...

# clear all parameters
minuit.Command("CLEAR")
# set title of the fit
minuit.Command("SET TIT TUTORIAL_MEAN")

# define fit parameters...
# we need an error flag for that
errfl = ctypes.c_int(0)
# param. nr., name, init. value, init. step size, low bound, high bound
minuit.mnparm(0, "mean", 0.0, 0.1, -10., 10., errfl)

# define the measurements and their errors - this may be a length, or multiple
# measurements of a resistance, or ...
data = [3.14, 3.15, 3.24, 2.79]
errs = [0.01, 0.01, 0.1, 1.0]

# covariances are errors squared
covs = [e * e for e in errs]
print covs

# and we'll need the inverse of the covariance
icovs = []
for cov in covs:
    icovs.append(1. / cov)

print icovs

# give MINUIT the function to minimise
minuit.SetFCN(fcn)

# and tell it to minimise fcn - up to 10k fcn evaluations, tolerance 0.001
minuit.Command("MIGRAD 10000 0.001")
# and run MINOS just after
minuit.Command("MINOS 10000 0.001")

# vim: sw=4:tw=78:ft=python:et
