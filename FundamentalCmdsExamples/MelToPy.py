import pymel.core as pymel
import pymel.tools.mel2py as mel2py
result = pymel.promptDialog(title = 'Convert Mel to Pymel', message = 'Enter Mel string: ', button = ['OK','Cancel'], defaultButton = 'OK', cancelButton = 'Cancel', dismissText = 'Cancel')

if result == 'OK':
	text = pymel.promptDialog(query = True, text = True)

	#get the pymel equivalent
	pymelAnswer = mel2py.mel2pyStr(text, pymelNamespace = 'mc')

	#get rid of the old way
	pymelCode = pymelAnswer.replace('pymel.all', 'maya.cmds')
	print(pymelCode)