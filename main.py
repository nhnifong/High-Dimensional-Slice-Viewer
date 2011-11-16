#!/usr/bin/env python
 
import sys
from PyQt4 import Qt, QtGui
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
		
		
	def paintEvent(self, event):
		# keep this function under 30ms
		w = self.size().width()
		h = self.size().height()
		qp = QtGui.QPainter()
		qp.begin(self)
		qp.setPen(QtGui.QColor(255, 100, 23))
		qp.setBrush(QtGui.QColor(255, 255, 184))
		qp.drawRect(0, 0, w-1, h-1)
		
		print time()
		
		qp.end()


app = Qt.QApplication(sys.argv)
app.setApplicationName("High Dimensional Slice Viewer")
widget = HDSV_Main()
widget.show()
app.exec_()