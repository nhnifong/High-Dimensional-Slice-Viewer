#!/usr/bin/env python
from __future__ import division
import numpy as np
from math import e,sin,cos
from scipy.spatial import KDTree

def sigmoid(x):
	return 1/(1+e**(-x))
	
class NumpyDataService:
	def __init__(self):
		self.data = np.fromfile("small.nparray",np.dtype('float64'))
		self.data.shape = (40000, 5)
		self.keys  = [0,1]
		
	def getDimensionality(self):
		return self.data.shape[0]
		
	def setKeyDimensions(self,keydims):
		# rebuild the kdtree on only the key dimensions
		self.kdtree = KDTree(self.data[:,keydims])
		self.keys = keydims
		
	def resolve(self,vec,requested):
		""" vec will be a vector with missing data [0.44, None, None 0.01, None] of the same
		Dimensionality as our dataset
		This function is responsible for filling in values for the requested dimensions
		requested will be a list of the form [1,2,4] where the numbers are dimensions
		
		One way to do this is to find the point closest to the mark in the provided dimensions
		And return it's values in the requested dimensions
		
		Another way would be to find all the points closer than a threshold and average them
		
		scipy.spatial.KDTree might be useful
		
		"""
		
		# whoa dude
		#for i in range(5):
		#	vec[i] = sigmoid((sin(vec[0]*20)+cos(vec[1]*30)))
		
		needed = [vec[k] for k in self.keys]
		assert (None not in needed)
		
		ans = self.kdtree.query(needed)
		vec = self.data[ans[1]]
			
		return vec