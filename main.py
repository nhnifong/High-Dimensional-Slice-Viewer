#!/usr/bin/env python
from __future__ import division
import sys
from PyQt4 import Qt, QtGui, QtCore
from time import time
from random import randint,random
from dataserv import NumpyDataService

class HDSV_Main(QtGui.QWidget):
	def __init__(self, parent=None):
		super(HDSV_Main, self).__init__(parent)
		self.parent = parent
		#set some general properties of the window
		self.setWindowTitle("High Dimensional Slice Viewer")
		self.setMinimumSize(200, 200)

		# Create sliceview Widget
		self.sliceview = SliceView(self)

		# layout GUI
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.sliceview)
		self.setLayout(vbox)
		
class SliceView(QtGui.QWidget):
	"""  This is the custom widget that does the slice drawing
	The method of drawing will be a steady approximation
	where the slice is resolved at a finer and finer resolution
	(in paralell if possible) until the there is a seperate
	data value for each pixel (depends on the size of the widget)
	"""
	def __init__(self, parent=None):
		super(SliceView, self).__init__(parent)
		self.parent = parent
		self.pixmap = None
		self.roxtimer = None
		self.dataService = NumpyDataService()
		# test file is a 5 by 10424000 matrix of values between 0 and 1
		# Its a picture of a pair of Chestnuts. each entry is (x,y,r,g,b)
		# right now its just serving as a dead simple "high dimensional" dataset
		
		# here is the mapping to the higer dimensional data
		self.sourceDimensionality = self.dataService.getDimensionality()
		# the list of dimensions in the HD space that each of the following
		# variables (x,y,r,g,b) is mapped to
		self.dim = [0,1,2,3,4]
		# the slope of the view in each of the possible source dimensions (NYI)
		self.slope = [1.0]*self.sourceDimensionality
		
	def paintEvent(self, event):
		""" This should return immediately duh
			Draw the pixmap the worker threads have been working on.
		"""
		qp = QtGui.QPainter()
		qp.begin(self)
		if self.pixmap!=None:
			qp.drawPixmap(0, 0, self.pixmap)
		qp.end()
		
	def restartRox(self):
		""" This method restarts the iterative refinement of the slice image
		It should be called whenever the slice-defining parameters change,
		and whenever the size of the slice view widget changes.
		should return immediately.
		"""
		self.roxtimer = QtCore.QTimer(self)
		self.connect(self.roxtimer, Qt.SIGNAL("timeout()"), self.addDetail);
		
		# init some variables needed by the iterative refinement
		self.timetopaint = time()
		self.numdp = 0
		
		# start the code!
		self.roxtimer.start(0)
		
	def addDetail(self):
		""" This method does all the work
		It takes the dimensional mapping and the slope, and requests data from the data service that
		indicate what color to draw tiny rectangles on self.pixmap
		
		Right now it just does 20 new data points eah time it's called, but a better strategy would
		be to start with at least one and just work until 10ms has passed.
		"""
		w = self.size().width()
		h = self.size().height()
		
		qp = QtGui.QPainter()
		qp.begin(self.pixmap)
		qp.setRenderHint(qp.Antialiasing,True)
		
		# investigate new data points
		stopworking = time()+0.01
		while time() < stopworking:
		
			locX = random()
			locY = random()
			
			# set up the hypothetical data point, and fill in the values we know
			# (the two that are mapping to the x and y coordinates of this view
			dat = [None]*self.sourceDimensionality
			dat[self.dim[0]] = locX * self.slope[self.dim[0]]
			dat[self.dim[1]] = locY * self.slope[self.dim[1]]
			# ask the data service to fill in values for the three dimensions
			# that correspond to red green an blue
			dat = self.dataService.resolve(dat,self.dim[-3:])
			# now use the retreived information to decide on the color
			rgb = [dat[self.dim[k]] / self.slope[self.dim[k]] * 255 for k in [2,3,4]]
			color = QtGui.QColor(*rgb)
			# increment number of data points for following calculation
			self.numdp += 1
			# size of the box we will draw around this data point is equal to the area of the
			# widget divided by the number of total data points already drawn including this one.
			sqside = (float(w*h)/self.numdp)**0.5
			
			# termination condition, once the size of the squares drawn is 0.25px, stop
			if sqside < 0.25:
				self.roxtimer.stop()
				self.repaint()
			
			# draw
			qp.setPen(color)
			qp.setBrush(color)
			qp.drawRect(QtCore.QRectF(locX*w-sqside*0.5, locY*h-sqside*0.5, sqside, sqside))
		
		
		qp.end()
		
		if self.timetopaint <= time():
			self.timetopaint = time() + 0.03
			self.repaint()
		
	def resizeEvent(self, event):
		self.pixmap = QtGui.QPixmap(event.size().width(), event.size().height())
		self.restartRox()
		


app = Qt.QApplication(sys.argv)
app.setApplicationName("High Dimensional Slice Viewer")
widget = HDSV_Main()
widget.show()
app.exec_()