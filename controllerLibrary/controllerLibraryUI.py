from controllerLibrary import ControllerLibrary # import the ControllerLibrary class from controllerLibrary.py
from Qt import QtWidgets, QtCore, QtGui # QtWidgets does not exist in pre-2016 Maya

class ControllerLibraryUI(QtWidgets.QDialog): # ControllerLibrary is a dialog inherited from QDialog
	def __init__(self):
		super(ControllerLibraryUI, self).__init__() # same as: QtWidgets.QDialog.__init__(self) but more flexible & scalable, can inherit from multiple classes
		self.setWindowTitle('Controller Library UI') 
		self.library = ControllerLibrary() # Store an instance of ControllerLibrary inside UI
		self.buildUI()
		self.populate()

	def buildUI(self):
		layout = QtWidgets.QVBoxLayout(self) # create master vertical box layout (maya column layout)
		saveWidget = QtWidgets.QWidget() # base class of all UI objects for the top save layout: save button & text field
		saveLayout = QtWidgets.QHBoxLayout(saveWidget) # horizontal box layout for saveWidget
		layout.addWidget(saveWidget)

		self.saveNameField = QtWidgets.QLineEdit() # use self to access the saveNameField later: variable accessible inside of class
		saveLayout.addWidget(self.saveNameField) # add text field to the saveWidget horizontal box layout 

		saveBtn = QtWidgets.QPushButton('Save')
		saveLayout.addWidget(saveBtn)

		self.listWidget = QtWidgets.QListWidget() # use self to access the list of thumbnails later
		layout.addWidget(self.listWidget)

		btnWidget = QtWidgets.QWidget()  # base class of all UI objects for the bottom horizontal buttons layout group
		btnLayout = QtWidgets.QHBoxLayout(btnWidget)
		layout.addWidget(btnWidget)
		importBtn = QtWidgets.QPushButton('Import')
		btnLayout.addWidget(importBtn)
		refreshBtn = QtWidgets.QPushButton('Refresh')
		btnLayout.addWidget(refreshBtn)
		closeBtn = QtWidgets.QPushButton('Close')
		btnLayout.addWidget(closeBtn)

	def populate(self):
		pass

def showUI():
	ui = ControllerLibraryUI() # create new instance
	ui.show()
	return ui