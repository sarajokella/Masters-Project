#!/usr/bin/env python

l = [7, 6, 12]

for first, second in zip(l, l):
	print first, second


import sys
import math
import ctypes
import ROOT

def patchROOTsVectorAndMatrix(typ):
    """ helper to patch some of the botched pythonization of ROOT 
matrix/vector classes """
    def add(typ, m1, m2):
        retVal = typ(m1)
        retVal += m2
        return retVal
    def sub(typ, m1, m2):
        retVal = typ(m1)
        retVal -= m2
        return retVal
    def mul(typ, a, b):
        if type(a) == float:
            retVal = typ(b)
            retVal *= a
        else:
            retVal = typ(a)
            retVal *= b
        return retVal
    typ.__add__ = lambda a, b: add(typ, a, b)
    typ.__sub__ = lambda a, b: sub(typ, a, b)
    typ.__mul__ = lambda a, b: mul(typ, a, b)

patchROOTsVectorAndMatrix(ROOT.TMatrixD)
patchROOTsVectorAndMatrix(ROOT.TMatrixDSym)
patchROOTsVectorAndMatrix(ROOT.TVectorD)

def makeTVectorD(list):
    """ build a TVectorD from a list """
    retVal = ROOT.TVectorD(len(list))
    for i in xrange(0, len(list)):
        retVal[i] = list[i]
    return retVal


def buildCovMatrix(errs, correl):
    """ build a covariance matrix from errors and a correlation matrix """
    if len(correl) != len(errs):
        raise "Error vector different length than correlation matrix"
    retVal = []
    for i in range(0, len(correl)):
        if len(correl[i]) != len(correl):
            raise "Matrix shape ill defined"
        retVal.append([])
        for j in xrange(0, len(correl)):
            retVal[i].append(correl[i][j] * errs[i] * errs[j])
    return retVal


def makeTMatrixDSym(mat):
    """ build a TMatrixD from a list of lists (python-style matrix) """
    retVal = ROOT.TMatrixDSym(len(mat))
    for i in xrange(0, len(mat)):
        if len(mat[i]) != len(mat):
            raise "Matrix shape ill defined"
        for j in xrange(0, len(mat)):
            retVal[i][j] = mat[i][j]
    return retVal


def invDet(mat):
    """ return inverse and determinant of a (covariance) matrix """
    imat = ROOT.TMatrixDSym(mat)
    decomp = ROOT.TDecompChol(mat)
    decomp.Invert(imat)
    det = 1.
    for i in xrange(0, mat.GetNrows()):
        det *= decomp.GetU()[i][i]
    return imat, det * det


def buildFullCovMatrix(errStat, correlStat, errSyst, correlSyst):
    return (makeTMatrixDSym(buildCovMatrix(errStat, correlStat)) +
            makeTMatrixDSym(buildCovMatrix(errSyst, correlSyst)))


def calcDsKVars(rDsK, delta, gamma, betas):
    def C(rDsK):
        return (1 - rDsK) * (1 + rDsK) / (1 + rDsK * rDsK)
    def ADG(rDsK, delta, gamma, betas):
        return (-2 * rDsK * math.cos(delta - (gamma - 2 * betas))) / (1 + rDsK * rDsK)
    def ADGbar(rDsK, delta, gamma, betas):
        return (-2 * rDsK * math.cos(delta + (gamma - 2 * betas))) / (1 + rDsK * rDsK)
    def S(rDsK, delta, gamma, betas):
        return (+2 * rDsK * math.sin(delta - (gamma - 2 * betas))) / (1 + rDsK * rDsK)
    def Sbar(rDsK, delta, gamma, betas):
        return (-2 * rDsK * math.sin(delta + (gamma - 2 * betas))) / (1 + rDsK * rDsK)

    return makeTVectorD([
        C(rDsK),
        ADG(rDsK, delta, gamma, betas),
        ADGbar(rDsK, delta, gamma, betas),
        S(rDsK, delta, gamma, betas),
        Sbar(rDsK, delta, gamma, betas), betas ])

def gauss(x, mu, icov, det):
   return math.exp(-0.5 * icov.Similarity(x - mu)) / math.sqrt(
            (2. * math.pi) ** icov.GetNrows() * det)

def evalpdf(pdf, *args):
    """
    Evaluate pdf with given arguments, protecting against failures.

    pdf     pdf to evaluate
    args    any number of arguments to pass to pdf

    Returns the value of the pdf, or a vanishingly tiny probability on
    failure.

    For example, using evalpdf(gauss, x, mu, sigma) will call
    gauss(x, mu, sigma), and return the result, or something tiny on error
    """
    retVal = pdf(*args)
    # check if value makes sense
    if retVal <= 0. or retVal != retVal:
        # no - replace by tiniest probability representable by a float,
        # and print a warning; if this happens, this usually indicates
        # something is wrong with the inputs, or the math inside pdf
        retVal = sys.float_info.min
        print("In evalpdf: invalid PDF value: %s%s = %f" % (str(pdf),
              str(args), retVal))
    return retVal


def fcn(npar, grad, retVal, par, flag):
    if 2 == flag:  # check if Minuit wants us to calculate gradient
        # indicate that that's not supported at the moment
        for i in xrange(0, npar[0]):
            grad[i] = float('NaN')
    # calculate the log LH sum over the data
    loglhsum = 0.
    for i in xrange(0, len(data)):  # loop over data
        # calculate PDF (a Gaussian) for data point i
        pdf = evalpdf(gauss, data[i], calcDsKVars(*[ par[j] for j in xrange(0, 4) ]), icovs[i], dets[i])
        loglhsum = loglhsum + math.log(pdf)
    # return - log LH
    retVal[0] = -loglhsum


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
minuit.mnparm(0, "rDsK" , 0.40, 0.1, 0.01, 10., errfl)
minuit.mnparm(1, "delta", 0.00, 0.1, -1. * math.pi, 1. * math.pi, errfl)
minuit.mnparm(2, "gamma", 1.22, 0.1, -1. * math.pi, 1. * math.pi, errfl)
minuit.mnparm(3, "betas", 0.00, 0.1, -1. * math.pi, 1. * math.pi, errfl)
minuit.SetErrorDef(0.5)

# define the measurements and their errors - this may be a length, or multiple
# measurements of a resistance, or ...
data = [
        makeTVectorD([0.53, 0.37, 0.2, -1.09, -0.36, -0.5 * 0.01 ])
        ]
covs = [
        buildFullCovMatrix(
            [ 0.25, 0.42, 0.41, 0.33, 0.34, 0.5 * 0.07 ], # stat. errors and correlation
            [ [  1.000,  0.084,  0.103, -0.008, -0.045, 0 ] ,
              [  0.084,  1.000,  0.544, -0.117, -0.022, 0 ],
              [  0.103,  0.544,  1.000, -0.067, -0.032, 0 ],
              [ -0.008, -0.117, -0.067,  1.000,  0.002, 0 ],
              [ -0.045, -0.022, -0.032,  0.002,  1.000, 0 ],
              [  0.000,  0.000,  0.000,  0.000,  0.000, 1 ]],
            [ 0.04, 0.20, 0.20, 0.08, 0.08, 0.5 * 0.01 ], # syst. error and correlation
            [ [  1.00,  0.22,  0.22, -0.04, -0.03, 0 ],
              [  0.22,  1.00,  0.96, -0.17, -0.14, 0 ],
              [  0.22,  0.96,  1.00, -0.17, -0.14, 0 ],
              [ -0.04, -0.17, -0.17,  1.00,  0.09, 0 ],
              [ -0.03, -0.14, -0.14,  0.09,  1.00, 0 ],
              [  0.00,  0.00,  0.00,  0.00,  0.00, 1 ]])
        ]

icovs = []
dets = []
for cov in covs:
    icov, det = invDet(cov)
    icovs.append(icov)
    dets.append(det)

# give MINUIT the function to minimise
minuit.SetFCN(fcn)

# and tell it to minimise fcn - up to 10k fcn evaluations, tolerance 0.001
minuit.Command("MIGRAD 10000 0.001")
# and run MINOS just after
minuit.Command("MINOS 10000 0.001")

def findUp(dChi2, ndf):
    # work out which confidence level a deltaChi2 away from the minimum means
    # for a one parameter fit
    CL = 1. - ROOT.TMath.Prob(dChi2, 1)
    # find what kind of a chi^2 increase that corresponds to in a fit with ndf
    # parameters; use bisection to find the right increase
    chi2lo, chi2hi = 1., 1e3
    lo = 1. - ROOT.TMath.Prob(chi2lo, ndf) - CL
    hi = 1. - ROOT.TMath.Prob(chi2hi, ndf) - CL
    while ((chi2hi - chi2lo) > 1e-6): # bisection loop
        chi2mid = 0.5 * (chi2lo + chi2hi)
        mid = 1. - ROOT.TMath.Prob(chi2mid, ndf) - CL
        if (lo * mid) < 0.:
            chi2hi, hi = chi2mid, mid
        elif (hi * mid) < 0.:
            chi2lo, lo = chi2mid, mid
        else:
            break
    return 0.5 * (chi2lo + chi2hi)


def plotContours(npar1, npar2, title, name1, name2, sigmas = [ 1., 2. ], colors = [ ROOT.kOrange, ROOT.kGreen, ROOT.kBlue ], npoints = 150):
    first = True
    sigmas = sorted(sigmas)
    sigmas.reverse()
    ndf = 2 # minuit.GetNumFreePars();
    ups = [ findUp(sigma * sigma, ndf) for sigma in sigmas ]
    print "DEBUG: sigmas %s ndf %u => dChi2 %s" % (str(sigmas), ndf, str(ups))
    for up, color in zip(ups, colors):
        minuit.SetErrorDef(0.5 * up)
        cont1 = minuit.Contour(npoints, npar1, npar2)
        cont1.SetLineColor(color)
        cont1.SetFillStyle(1001)
        cont1.SetFillColor(color - 3)
        cont1.SetMarkerColor(color)
        cont1.SetMarkerStyle(0)
        cont1.SetMarkerSize(0)
        cont1.SetTitle("%s;%s;%s" % (title, name1, name2))
        cont1.Draw("ACF" if first else "CFSAME")
        first = False
    x, y, e = ROOT.Double(0.), ROOT.Double(0.), ROOT.Double(0.)
    minuit.GetParameter(npar1, x, e)
    minuit.GetParameter(npar2, y, e)
    m = ROOT.TMarker(x, y, 29)
    m.SetMarkerSize(2.5)
    m.Draw("SAME")
    c1.Print("cont_%d_%d.pdf" % (npar1, npar2))


c1 = ROOT.TCanvas()
#plotContours(2, 0, "contours #gamma vs. r_{D_{s} K}", "#gamma [rad]", "r_{D_{s} K}")
#plotContours(2, 1, "contours #gamma vs. #delta", "#gamma [rad]", "#delta [rad]")







