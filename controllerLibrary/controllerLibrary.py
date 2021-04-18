from maya import cmds
import os
import json
import pprint

USER_APP_DIR = cmds.internalVar(userAppDir = True) # user's maya app directory
DIRECTORY = os.path.join(USER_APP_DIR, 'controllerLibrary') # use os specific separator (different between Windows/Mac/Linux)

# create the library directory. if function is not given any value: it will use the default directory
def createDirectory(directory = DIRECTORY):
	"""
	Creates the given directory if it doesn't exist already
	Args:
	directory(str): the directory to create
	"""

	# if this directory does not exist: make this directory
	if not os.path.exists(directory):
		os.mkdir(directory)

# class to manage controllers: find existing saved controllers & save new controllers
class ControllerLibrary(dict):
	def save(self, name, directory = DIRECTORY):
		createDirectory(directory)
		path = os.path.join(directory, '%s.ma' % name)

		cmds.file(rename = path)
		if cmds.ls(selection = True): # if there's a selection: get a list of the selections
			cmds.file(force = True, type = 'mayaAscii', exportedSelected = True)
		else:
			cmds.file(save = True, type = 'mayaAscii', force = True) # if the file already exists: force save over it
	
	# method to find any controller .ma files that has been saved
	def find(self, directory = DIRECTORY):
		if not os.path.exists(directory):
			return

		files = os.listdir(directory)
		mayaFiles = [mayafile for mayafile in files if mayafile.endswith('.ma')] # avoid using file keyword in python

		# loop through maya files & add them to the dictionary, linking to the file path
		for ma in mayaFiles:
			name, extension = os.path.splitext(ma) # split the extension from the file, give back name & extension - just print file name without extension
			path = os.path.join(directory, ma)
			self[name] = path # inherit from dict: can access cells as if it's a dictionary

		pprint.pprint(self) # print key & value in a pretty easy to read manner
