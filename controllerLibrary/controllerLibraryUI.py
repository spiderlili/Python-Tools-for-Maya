from controllerLibrary import ControllerLibrary # import the ControllerLibrary class from controllerLibrary.py
from Qt import QtWidgets, QtCore, QtGui # QtWidgets does not exist in pre-2016 Maya

class ControllerLibraryUI(QtWidgets.QDialog): # ControllerLibrary is a dialog inherited from QDialog
	def __init__(self):
		super(ControllerLibraryUI, self).__init__() # same as: QtWidgets.QDialog.__init__(self) but more flexible & scalable, can inherit from multiple classes
		self.setWindowTitle('Controller Library UI') 
		self.library = ControllerLibrary() # Store an instance of ControllerLibrary inside UI
		self.buildUI()
		self.populate()

def showUI():
	ui = ControllerLibraryUI() # create new instance
	ui.show()