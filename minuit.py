#!/usr/bin/env python
#
# little example using minuit to calculate the mean of a bunch of measurements
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
   # for i in xrange(0, len(alpha)):  # loop over data
    if par[1]!= 0.0:
    	a1 = par[0]/par[1]
    	a2 = (1-par[0])/par[1]
    	achi = (alpha - (math.atan(a1) + math.atan(a2)))/ealpha
    if (1-par[0]) != 0.0:	
	b1 = par[1]/(1-par[0])
	bchi = (beta -(math.atan(b1)))/ebeta
    if par[0]!= 0.0:
	gchi = math.atan(par[1]/par[0])
    chi2sum = chi2sum + achi*achi + bchi*bchi + gchi*gchi    
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
minuit.mnparm(0, "rhobar", 0.1, 0.1, 0.0, 0.5, errfl)
minuit.mnparm(1, "etabar", 0.1, 0.1, 0.0, 0.5, errfl)

# define the measurements and their errors - this may be a length, or multiple
# measurements of a resistance, or ...
alpha = 95.8*math.pi/180
ealpha = 7*math.pi/180
beta = 21.2*math.pi/180
ebeta = 1*math.pi/180
gamma = 82*math.pi/180
egamma = 20*math.pi/180

# give MINUIT the function to minimise
minuit.SetFCN(fcn)

# and tell it to minimise fcn - up to 10k fcn evaluations, tolerance 0.001
minuit.Command("MIGRAD 10000 0.001")
# and run MINOS just after
minuit.Command("MINOS 10000 0.001")

c1 = ROOT.TCanvas() #Draw a contour map of the two parameters
minuit.SetPrintLevel(0)

colour = [ROOT.kBlue, ROOT.kRed]
parms = ["#bar{#rho}", "#bar{#eta}"]

for n in range(0,len(parms)):
	minuit.SetErrorDef(2*2)
	x = 0
	cont = minuit.Contour(150, x, 1)
	cont.SetLineColor(ROOT.kBlue)
	cont.SetTitle("Contour Graph of " + parms[n-2] + " vs " + parms[n-1])
	cont.GetYaxis().SetTitle(parms[n-2])
	cont.GetYaxis().SetTitleOffset(1.4)
	cont.GetXaxis().SetTitle(parms[n-1])
	cont.Draw()
	minuit.SetErrorDef(1*1)
	cont2 = minuit.Contour(150, x, 1)
	cont2.SetLineColor(ROOT.kRed)
	cont2.Draw("SAME")
	x = x + 1

#minuit.SetErrorDef(2*2)
#cont = minuit.Contour(50, 0, 1)
#cont.SetLineColor(ROOT.kBlue)
#cont.SetTitle("Contour Graph of #bar{#rho} vs #bar#eta")
#cont.GetYaxis().SetTitle("#bar#rho")
#cont.GetYaxis().SetTitleOffset(1.4)
#cont.GetXaxis().SetTitle("#bar#eta")
#cont.Draw()


#minuit.SetErrorDef(1*1)
#cont2 = minuit.Contour(150, 0, 1)
#cont2.SetLineColor(ROOT.kRed)
#cont2.Draw("SAME")

x,y,e = ROOT.Double(0.), ROOT.Double(0.), ROOT.Double(0.) #Add the parameter point
minuit.GetParameter(0, x, e)
minuit.GetParameter(1, y, e)
m = ROOT.TMarker(x, y, 30)
m.SetMarkerSize(2.5)
m.Draw("SAME")
c1.Print("contourgraph.pdf")

# vim: sw=4:tw=78:ft=python:et

