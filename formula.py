#!/usr/bin/env python

import sys
import math

def Cpipi(d, theta, gamma):
	x = -(2*d*math.sin(theta)*math.sin(gamma))/(1 - 2*d*math.cos(theta)*math.cos(gamma)+d*d)
	return x

def Spipi(d, theta, gamma, beta):
	x = -(math.sin(2*beta+2*gamma)-2*d*math.cos(theta)*math.sin(2*beta+gamma)+d*d*math.sin(2*beta))/(1-2*d*math.cos(theta)*math.cos(gamma)+d*d)
	return x

def Ckk(dprimetilde, thetaprime, gamma):
	x = (2*dprimetilde*math.sin(thetaprime)*math.sin(gamma))/(1+2*dprimetilde*math.cos(thetaprime)*math.cos(gamma)+dprimetilde**2)
	return x

def Skk(dprimetilde, thetaprime, gamma, betas):
	x = -(math.sin(-2*betas+2*gamma)+2*dprimetilde*math.cos(thetaprime)*math.sin(-2*betas+gamma)+dprimetilde*dprimetilde*math.sin(-2*betas))/(1+2*dprimetilde*math.cos(thetaprime)*math.cos(gamma)+dprimetilde**2)
	return x

def Akk(dprimetilde, thetaprime, gamma, betas):
	x = -(math.cos(2*betas+2*gamma)+2*dprimetilde*math.cos(thetaprime)*math.cos(2*betas+gamma)+dprimetilde*dprimetilde*math.cos(2*betas))/(1+2*dprimetilde*math.cos(thetaprime)*math.cos(gamma)+dprimetilde**2)
	return x

#print Cpipi(0.3, 3.6652, 1.134)
#print Spipi(0.3, 3.6652, 1.13, 0.3929)
#print Ckk(5.64, 3.6652, 1.13)
#print Skk(5.64, 3.6652, 1.13, 0.000321)

chi2sum = 0

rad = math.pi/180

Cpi = -0.34
Spi = -0.63
Ck = 0.20
Sk = 0.18
eCpi = 0.06
eSpi = 0.05
eCk = 0.06
eSk = 0.06
Ak = -0.79
eAk = 0.07

lambdaCKM = 0.2247
elambda = 0.00025

beta = 22.5*rad
ebeta = 0.55*rad
betas = 0.01843*rad
ebetas = 0.00048*rad

d = 0.3
theta = 210*rad
gamma = 65*rad

dprimetilde = d*((1-lambdaCKM*lambdaCKM)/(lambdaCKM*lambdaCKM))

cpipi = (Cpi - Cpipi(d, theta, gamma))/eCpi
spipi = (Spi - Spipi(d, theta, gamma, beta))/eSpi
ckk = (Ck - Ckk(dprimetilde, theta, gamma))/eCk
skk = (Sk - Skk(dprimetilde, theta, gamma, betas))/eSk

print chi2sum + cpipi**2 + spipi**2 + ckk**2 + skk**2 # + akk**2

#682.0988
#0.349287
