#!/usr/bin/env python
#
# little example using minuit to calculate the mean of a bunch of measurements
import sys
import math
import scipy
import ctypes
import numpy as np
import ROOT
from formula import Cpipi, Spipi, Ckk, Skk
from Covariance import Covinv
import re

def fcn(npar, grad, retVal, par, flag):


    if 2 == flag:  # check if Minuit wants us to calculate gradient
        # indicate that that's not supported at the moment

    	for i in xrange(0, npar[0]):
    		grad[i] = float('NaN')

    # calculate the chi^2 sum over the data
    chi2sum = 0.

    d = par[0]
    theta = par[1]
    gamma = par[2]
    dprimetilde = d*((1-lambdaCKM*lambdaCKM)/(lambdaCKM*lambdaCKM))

    v = [(Cpi-Cpipi(d,theta,gamma)), (Spi-Spipi(d,theta,gamma,beta)), (Ck-Ckk(dprimetilde,theta,gamma)), (Sk-Skk(dprimetilde,theta,gamma,betas))]

    chi2sum = np.dot(np.dot(v,Cinv),np.transpose(v))
    retVal[0] = chi2sum

# create a minimiser for 1 parameter
minuit = ROOT.TMinuit(1)
minuit.Command("SET PRINTOUT 1")  # tell it to be verbose...minuit.Command("SET WARNINGS")    # and to emit warnings...
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
minuit.mnparm(0, "d", 0.3, 0.1, 0.0, 0.9, errfl)
minuit.mnparm(1, "theta", 90*rad, 0.1, 0, 1. * math.pi, errfl)
minuit.mnparm(2, "gamma", 1.134, 0.1, 0, 1. * math.pi, errfl)

# define the measurements and their errors - this may be a length, or multiple
# measurements of a resistance, or ...
Cpi = -0.34
Spi = -0.63
Ck = 0.20
Sk = 0.18
Ak = -0.79

lambdaCKM = 0.2247
elambda = 0.00025

beta = 22.5*rad
ebeta = 0.55*rad
betas = 0.01843
ebetas = 0.00048

c = scipy.array([[1,0.448,-0.006,-0.009], [0.448,1,-0.04,-0.006], [-0.006,-0.040,1,-0.014], [-0.009,-0.006,-0.014,1]])
sys = scipy.array([0.06,0.05,0.06,0.06])
Cinv = Covinv(4,c,sys)

# give MINUIT the function to minimise
minuit.SetFCN(fcn)

# and tell it to minimise fcn - up to 10k fcn evaluations, tolerance 0.001
minuit.Command("MIGRAD 10000 0.001")
# and run MINOS just after
minuit.Command("MINOS 10000 0.001")

minuit.SetPrintLevel(0)

def Contours(par1, par2, yaxis, xaxis):
	c1 = ROOT.TCanvas()
	minuit.SetErrorDef(2*2)
	cont = minuit.Contour(150, par1, par2)
	cont.SetLineColor(ROOT.kBlue)
	cont.GetYaxis().SetTitle(yaxis)
	cont.GetXaxis().SetTitle(xaxis)
	cont.SetTitle("Contour Graph of " + yaxis + " vs " + xaxis)
	cont.Draw()
	minuit.SetErrorDef(1*1)
	cont2 = minuit.Contour(150, par1, par2)
	cont2.SetLineColor(ROOT.kRed)
	cont2.Draw("SAME")

	x,y,e = ROOT.Double(0.), ROOT.Double(0.), ROOT.Double(0.)
	minuit.GetParameter(par1, x, e)
	minuit.GetParameter(par2, y, e)
	m = ROOT.TMarker(x, y, 30)
	m.SetMarkerSize(2.5)
	m.Draw("SAME")
	name = yaxis + "_" + xaxis + "_graph2.pdf"

	if re.search("#", name) != None:
		name = name.replace("#", "") 
		c1.Print(name)

	else:
		c1.Print(name)

Contours(1, 0, "d", "#theta")
Contours(2, 0, "d", "#gamma")
Contours(2, 1, "#theta", "#gamma")
