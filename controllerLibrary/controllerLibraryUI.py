from maya import cmds
import pprint
import controllerLibrary # import the ControllerLibrary class and not be bound to an instance from controllerLibrary.py
reload(controllerLibrary) # any code changes in the ControllerLibrary module will automatically be picked up by the UI

from Qt import QtWidgets, QtCore, QtGui # QtWidgets does not exist in pre-2016 Maya

class ControllerLibraryUI(QtWidgets.QDialog): # ControllerLibrary is a dialog inherited from QDialog
	"""
	A dialog which lets you save and import controllers
	"""
	def __init__(self):
		super(ControllerLibraryUI, self).__init__() # same as: QtWidgets.QDialog.__init__(self) but more flexible & scalable, can inherit from multiple classes
		self.setWindowTitle('Controller Library UI') 
		self.library = controllerLibrary.ControllerLibrary() # points to an instance of ControllerLibrary inside UI from controllerLibrary.py

		# everytime when creating a new instance: automatically build UI & populate it
		self.buildUI()
		self.populate()

	def buildUI(self):
		"""
		Build out the UI with master layout, child horizontal save widget, grid list widget to display controller thumbnails and child button holder widget
		"""
		# create master vertical box layout (maya column layout)
		layout = QtWidgets.QVBoxLayout(self) 

		# child horizontal widget: base class of all UI objects for the top save layout - save button & text field
		saveWidget = QtWidgets.QWidget() 
		saveLayout = QtWidgets.QHBoxLayout(saveWidget) # horizontal box layout for saveWidget
		layout.addWidget(saveWidget)

		self.saveNameField = QtWidgets.QLineEdit() # use self to access the saveNameField later: variable accessible inside of class
		saveLayout.addWidget(self.saveNameField) # add text field to the saveWidget horizontal box layout 

		saveBtn = QtWidgets.QPushButton('Save')
		saveBtn.clicked.connect(self.save)
		saveLayout.addWidget(saveBtn)

		# parameters for the thumbnail size
		iconSize = 64 # want icons to be 64 pixels wide
		bufferSpace = 12 

		# create a grid list widget to display controller thumbnails
		self.listWidget = QtWidgets.QListWidget() # use self to access the list of thumbnails later
		self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode) # display the view mode in icon mode
		self.listWidget.setIconSize(QtCore.QSize(iconSize, iconSize))
		self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust) # make the list grow & shrink with the window size
		self.listWidget.setGridSize(QtCore.QtSize(iconSize + bufferSpace, iconSize + bufferSpace)) # add buffer spacing between the icons
		layout.addWidget(self.listWidget)

		# child widget which holds all the buttons: base class of all UI objects for the bottom horizontal buttons layout group
		btnWidget = QtWidgets.QWidget()  
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
		"""
		Clear the listWidget and repopulate it with the contents of the controller library
		"""
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

			item.setToolTip(pprint.pformat(info)) # add a tooltip for each item in the list

	def load(self): 
		"""
		Load all the currently selected controllers
		"""
		currentSelectedItem = self.listWidget.currentItem()

		#safeguard if nothing is selected. TODO: display warning
		if not currentSelectedItem:
			cmds.warning("Nothing is selected!")
			return

		name = currentSelectedItem.text()
		self.library.load(name)

	def save(self):
		"""
		Save the controller with the given file name
		"""
		name = self.saveNameField().text
		# strip string of empty white spaces so it doesn't register as true in python. issue a warning if the name doesn't exist after stripping
		if not name.strip():
			cmds.warning("A name must be specified for the controller!")
			return

		self.library.save(name)
		self.populate() # refresh the view
		self.saveNameField.setText('') # reset the text to nothing

def showUI():
	"""
	Show and return a handle to the UI
	Returns: QDialog
	"""
	ui = ControllerLibraryUI() # create new instance
	ui.show()
	return ui