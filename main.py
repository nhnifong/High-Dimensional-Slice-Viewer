#!/usr/bin/env python
from __future__ import division
import sys
from PyQt4 import Qt, QtGui, QtCore
from time import time
from random import randint,random


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
		w = self.size().width()
		h = self.size().height()
		
		
		qp = QtGui.QPainter()
		qp.begin(self.pixmap)
		qp.setRenderHint(qp.Antialiasing,True)
		
		# investigste n new data points
		for n in range(20):
		
			pixelX = random()*w
			pixelY = random()*h
			dat = random()
			color = self.colorRamp(dat)
			self.numdp += 1
			
			# size of the box we will draw around this data point is equal to the area of the
			# widget divided by the number of total data points already drawn including this one.
			sqside = (float(w*h)/self.numdp)**0.5
			
			# termination condition, once the size of the squares drawn is 1px, draw only w*h*2 more
			if sqside < 0.25:
				self.roxtimer.stop()
				self.repaint()
			
			
			qp.setPen(color)
			qp.setBrush(color)
			qp.drawRect(QtCore.QRectF(pixelX-sqside*0.5, pixelY-sqside*0.5, sqside, sqside))
		
		
		qp.end()
		
		if self.timetopaint <= time():
			self.timetopaint = time() + 0.03
			self.repaint()
		
	def resizeEvent(self, event):
		self.pixmap = QtGui.QPixmap(event.size().width(), event.size().height())
		self.restartRox()
		
	def colorRamp(self,realNumber):
		x = int(realNumber*255)
		return QtGui.QColor(x, x, x)
		


app = Qt.QApplication(sys.argv)
app.setApplicationName("High Dimensional Slice Viewer")
widget = HDSV_Main()
widget.show()
app.exec_()