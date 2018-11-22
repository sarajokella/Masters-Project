#!/usr/bin/env python

"""
Determines covariance matrix from correlation matrix and systematic and
statistical uncertainties and finds its inverse using Cholesky
decomposition
"""

import scipy
import scipy.linalg
import numpy as np

def Covinv(dim, c, sys):

	"""
	dim = dimensions of correlation matrix
	c = correlation matrix
	sys = systematic errors as (eCpipi, eSpipi,...)
	"""

	C = np.zeros((dim,dim))

	for i in range(0,4):
		for j in range(0,4):
			C[i][j] = sys[i]*sys[j]*c[i][j]

	L = scipy.linalg.cholesky(C, lower = True)
	U = scipy.linalg.cholesky(C, lower = False)
	Cinv = np.dot(np.linalg.inv(U), np.linalg.inv(L)) #+np.identity(4)

	return Cinv

#c = scipy.array([[1, 0.448, -0.006, -0.009], [0.448, 1, -0.04, -0.006], [-0.006, -0.040, 1, -0.014], [-0.009, -0.006, -0.014, 1]])
#sys = scipy.array([0.06,0.05,0.06,0.06])

#print (Covinv(4, c, sys))

