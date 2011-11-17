#!/usr/bin/env python
 
import sys
from PyQt4 import Qt, QtGui, QtCore
from time import time


class HDSV_Main(QtGui.QWidget):
	def __init__(self, parent=None):
		super(HDSV_Main, self).__init__(parent)
		self.parent = parent
		#set some general properties of the window
		self.setWindowTitle("High Dimensional Slice Viewer")
		self.setMinimumSize(300, 300)

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
	def __inti__(self, parent=None):
		super(SliceView, self).__inti__(parent)
		self.parent = parent
		self.pixmap = None
		self.roxtimer = None
		
	def paintEvent(self, event):
		""" This should return immediately duh
			Draw the pixmap the worker threads have been working on.
		"""
		print time(),"painting"
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
		print "Say what again mothafucka I dare you!"
		self.roxtimer = QtCore.QTimer(self)
		self.connect(self.roxtimer, Qt.SIGNAL("timeout()"), self.addDetail);
		self.roxtimer.start(1000)
		
	def addDetail(self):
		print "What?"
		
	def resizeEvent(self, event):
		print time(),"resizing"
		self.pixmap = QtGui.QPixmap(event.size().width(), event.size().height())
		self.restartRox()
		


app = Qt.QApplication(sys.argv)
app.setApplicationName("High Dimensional Slice Viewer")
widget = HDSV_Main()
widget.show()
app.exec_()