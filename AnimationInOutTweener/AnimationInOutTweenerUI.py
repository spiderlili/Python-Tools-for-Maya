from maya import cmds

def tween(percentage, obj = None, attr = None, selection = True):
	# if obj is not given & selection is set to false: error
	if not obj and not selection:
		raise ValueError("No object is assigned to tween!")

	# if no obj is specified: get it from the 1st selection
	if not obj:
		obj = cmds.ls(selection = True)[0]

	# query the object from selection & list all keyable attributes
	if not attr:
		attr = cmds.listAttr(obj, keyable = True)

	currentTime = cmds.currentTime(query = True)
	print currentTime

tween(60)