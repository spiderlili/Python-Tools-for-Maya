from maya import cmds
import controllerLibrary # import the ControllerLibrary class and not be bound to an instance from controllerLibrary.py
reload(controllerLibrary) # any code changes in the ControllerLibrary module will automatically be picked up by the UI

from Qt import QtWidgets, QtCore, QtGui # QtWidgets does not exist in pre-2016 Maya

class ControllerLibraryUI(QtWidgets.QDialog): # ControllerLibrary is a dialog inherited from QDialog
	def __init__(self):
		super(ControllerLibraryUI, self).__init__() # same as: QtWidgets.QDialog.__init__(self) but more flexible & scalable, can inherit from multiple classes
		self.setWindowTitle('Controller Library UI') 
		self.library = controllerLibrary.ControllerLibrary() # Store an instance of ControllerLibrary inside UI from controllerLibrary.py
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
		saveBtn.clicked.connect(self.save)
		saveLayout.addWidget(saveBtn)

		iconSize = 64 # want icons to be 64 pixels wide
		bufferSpace = 12 
		self.listWidget = QtWidgets.QListWidget() # use self to access the list of thumbnails later
		self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode) # display the view mode in icon mode
		self.listWidget.setIconSize(QtCore.QSize(iconSize, iconSize))
		self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust) # make the list grow & shrink with the window size
		self.listWidget.setGridSize(QtCore.QtSize(iconSize + bufferSpace, iconSize + bufferSpace)) # add buffer spacing between the icons
		layout.addWidget(self.listWidget)

		btnWidget = QtWidgets.QWidget()  # base class of all UI objects for the bottom horizontal buttons layout group
		btnLayout = QtWidgets.QHBoxLayout(btnWidget)
		layout.addWidget(btnWidget)

		importBtn = QtWidgets.QPushButton('Import')
		importBtn.clicked.connect(self.load)
		btnLayout.addWidget(importBtn)

		refreshBtn = QtWidgets.QPushButton('Refresh')
		refreshBtn.clicked.connect(self.populate()) # repopulate the UI if any changes happen on disk - stay up to date
		btnLayout.addWidget(refreshBtn)

		closeBtn = QtWidgets.QPushButton('Close')
		closeBtn.clicked.connect(self.close) # when the closed button is clicked: connect the clicked signal to its close function defined in QDialog
		btnLayout.addWidget(closeBtn)

	def populate(self):
		self.listWidget.clear() # clear listWidget's contents to prevent adding duplicates
		self.library.find()
		for name, info in self.library.items(): # name = key, info = value
			item = QtWidgets.QListWidgetItem(name) # display string for the name 
			self.listWidget.addItem(item) 

			# add a screenshot to each of the elements, get the screenshot from the info dictionary
			screenshot = info.get('screenshot')
			if screenshot:
				icon = QtGui.QIcon(screenshot)
				item.setIcon(icon)

	# load all the selected controllers 
	def load(self): 
		currentSelectedItem = self.listWidget.currentItem()

		#safeguard if nothing is selected. TODO: display warning
		if not currentSelectedItem:
			cmds.warning("Nothing is selected!")
			return

		name = currentSelectedItem.text()
		self.library.load(name)

	def save(self):
		name = self.saveNameField().text
		# strip string of empty white spaces so it doesn't register as true in python. issue a warning if the name doesn't exist after stripping
		if not name.strip():
			cmds.warning("A name must be specified!")
			return

		self.library.save(name)
		self.populate() # refresh the view
		self.saveNameField.setText('') # reset the text to nothing

def showUI():
	ui = ControllerLibraryUI() # create new instance
	ui.show()
	return ui