#!/usr/bin/env python

#Adds errors for uncorrelated parameters to correlation matrix

import numpy as np

# dimf = dimensions of covariance matrix
# f = covariance matrix
# numberofparameters = number of uncorrelated parameters to add
# errorlist = list of parameter errors

def errors(dimf, f, numberofparameters, errorlist):
	f = f.tolist()

	for i in range(0, dimf):
		x = 0
		while x < numberofparameters:
			f[i].append(0)
			x = x + 1
	f = np.asarray(f)

	y = 0
	while y < numberofparameters:
		f = np.vstack([f, np.zeros(numberofparameters + dimf)])
		y = y + 1

	for i in range(0, numberofparameters):
		f[i+4][i+4] = errorlist[i]**2

	return f

