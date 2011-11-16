#!/usr/bin/env python
 
import sys
from PyQt4 import Qt

app = Qt.QApplication(sys.argv)
lbl = Qt.QLabel('Hello World')
lbl.show()
app.exec_()