from maya import cmds
import os
import json
import pprint

USER_APP_DIR = cmds.internalVar(userAppDir = True) # user's maya app directory
DIRECTORY = os.path.join(USER_APP_DIR, 'controllerLibrary') # use os specific separator (different between Windows/Mac/Linux)

# create the controller library directory. if function is not given any value: it will use the default directory
def createDirectory(directory = DIRECTORY):
	"""
	Creates the given directory if it doesn't exist already
	Args:
	directory(str): the directory to create
	"""

	# if this directory does not exist: make this directory
	if not os.path.exists(directory):
		os.mkdir(directory)

# core logic class to manage controllers: find existing saved controllers & save new controllers, user can specify any data they want to save
class ControllerLibrary(dict):
	def save(self, name, directory = DIRECTORY, screenshot = True, **info):
		createDirectory(directory)
		path = os.path.join(directory, '%s.ma' % name)

		# create a dictionary to save file data for the controller: file name & file path
		infoFile = os.path.join(directory, '%s.json' % name)
		info['name'] = name
		info['path'] = path

		cmds.file(rename = path)
		if cmds.ls(selection = True): # if there's a selection: get a list of the selections
			cmds.file(force = True, type = 'mayaAscii', exportedSelected = True)
		else:
			cmds.file(save = True, type = 'mayaAscii', force = True) # if the file already exists: force save over it

		if screenshot:
			info['screenshot'] = self.saveScreenshot(name, directory = directory)

		with open(infoFile, 'w') as f: # open the info file in write mode, store in temp f variable
			json.dump(info, f, indent = 4) # dump info dict into f (opened file stream), write data to file
	
		self[name] = info # always update the library everytime you save, prevent bugs

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
			
			infoFile = '%s.json' % name
			if infoFile in files:
				infoFile = os.path.join(directory, infoFile)

				with open(infoFile, 'r') as f: # open the info file stream in read mode, store info 
					info = json.load(f)
			else:
				info = [] # if do not find the json file: init empty dictionary

			screenshot = '%s.jpg' % name
			if screenshot in files:
				info['screenshot'] = os.path.join(directory, name)

			# populate the dictionary in case the information is not there
			info['name'] = name
			info['path'] = path

			self[name] = info # inherit from dict: can access cells as if it's a dictionary

		pprint.pprint(self) # print key & value in a pretty easy to read manner

	# load the saved controller file back inside maya, give it a file name string 'name' to load
	def load(self, name):
		path = self[name]['path'] # query dictionary object's path value - self[name] returns a dictionary object(NOT the path)
		cmds.file(path, i = True, usingNamespaces = False) # python does not allow import keyword - use i instead. does not import controller into new namespace

	def saveScreenshot(self, name, directory = DIRECTORY):
		path = os.path.join(directory, '%s.jpg' % name)
		cmds.viewFit() # make sure the view fits exactly around the controller
		cmds.setAttr('defaultRenderGlobals.imageFormat', 8) # save to jpeg format
		cmds.playblast(completeFilename = path, forceOverwrite = True, format = 'image', width = 200, height = 200, showOrnaments = False, startTime = 1, endTime = 1, viewer = False)
		return path
