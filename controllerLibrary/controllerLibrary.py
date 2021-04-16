# goal: create the library directory

from maya import cmds
import os
import json
import pprint

USER_APP_DIR = cmds.internalVar(userAppDir = True) # user's maya app directory
DIRECTORY = os.path.join(USER_APP_DIR, 'controllerLibrary') # use os specific separator (different between Windows/Mac/Linux)

# if function is not given any value: it will use the default directory
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
