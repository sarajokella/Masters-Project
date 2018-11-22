#!/usr/bin/env python
#
# little example using minuit to calculate the mean of a bunch of measurements
import sys
import math
import ctypes
import ROOT
from formula import Cpipi, Spipi, Ckk, Skk


def fcn(npar, grad, retVal, par, flag):


    if 2 == flag:  # check if Minuit wants us to calculate gradient
        # indicate that that's not supported at the moment
    	for i in xrange(0, npar[0]):
    		grad[i] = float('NaN')
    # calculate the chi^2 sum over the data
    chi2sum = 0.
   # for i in xrange(0, len(alpha)):  # loop over data
    d2 = (1-lamda*lamda)/(lamda*lamda)
    num1 = -2*par[1]*math.sin(par[2])*math.sin(par[0])
    num2 = (-math.sin(2*beta + 2*par[0]) - 2*par[1]*math.cos(par[2])*math.sin(2*beta+par[0])+par[1]*par[1]*math.sin(2*beta))        
    num3 = (-2*par[1]*d2*math.sin(par[2])*math.sin(par[0]))
    num4 = (-math.sin(2*betas+2*par[0])-2*par[1]*d2*math.cos(par[2])*math.sin(2*betas+par[0])+par[1]*par[1]*d2*d2*math.sin(2*betas))

    den = 1 - 2*par[1]*math.cos(par[2])*math.cos(par[0]) + par[1]*par[1]
    den1 = 1 - 2*par[1]*d2*math.cos(par[2])*math.cos(par[0]) + par[1]*par[1]*d2*d2

    if den!= 0.0:
    	Cpichi = (Cpi - (num1/den))/eCpi
    	Spichi = (Spi - (num2/den))/eSpi
        Ckchi = (Ck - (num2/den1))/eCk
        Skchi = (Sk - (num4/den1))/eSk
    chi2sum = chi2sum + Cpichi*Cpichi + Spichi*Spichi + Ckchi*Ckchi + Skchi*Skchi
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

rad = math.pi/180

# define fit parameters...
# we need an error flag for that
errfl = ctypes.c_int(0)

# param. nr., name, init. value, init. step size, low bound, high bound
minuit.mnparm(0, "gamma", 65*rad, 0.1, 0, 180*rad, errfl)
minuit.mnparm(1, "d", 0.3, 0.1, 0.0, 0.9, errfl)
minuit.mnparm(2, "theta", 210*rad, 1.0, 0.0, 270*rad, errfl)

# define the measurements and their errors - this may be a length, or multiple
# measurements of a resistance, or ...
Cpi = -0.34
Spi = -0.63
Ck = 0.20
Sk = 0.18
eCpi = 0.06
eSpi = 0.05
eCk = 0.06
eSk = 0.06

lamda = 0.2247
elamda = 0.00025

beta = 22.5*rad
ebeta = 0.55*rad
betas = 0.01843*rad
ebetas = 0.00048*rad #NOT SURE ABOUT *rad FOR ERRORS

# give MINUIT the function to minimise
minuit.SetFCN(fcn)

# and tell it to minimise fcn - up to 10k fcn evaluations, tolerance 0.001
minuit.Command("MIGRAD 10000 0.001")
# and run MINOS just after
minuit.Command("MINOS 10000 0.001")

#c1 = ROOT.TCanvas()
minuit.SetPrintLevel(0)

#minuit.SetErrorDef(1*1)
#cont = minuit.Contour(150, 1, 2)
#cont.SetLineColor(ROOT.kBlue)
#cont.Draw()
#c1.Print("d_theta_graph.pdf")

# vim: sw=4:tw=78:ft=python:et
