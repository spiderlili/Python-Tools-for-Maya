from maya import cmds

def rename():
	selection = cmds.ls(selection = True)

	'''get a new selection'''
	if len(selection) == 0: 
		selection = cmds.ls(dag = True, long = True) 

	'''sort using the length of the objects because children will have a longer full name: act on them first to not affect their path'''
	selection.sort(key = len, reverse = True) 
	'''print selection'''

	'''sort using the length of the objects because children will have a longer full name: act on them first to not affect their path'''
	for obj in selection:
		shortName = obj.split("|")[-1] 
		'''print shortName'''
		children = cmds.listRelatives(obj, children = True, fullPath = True) or [] 
		if len(children) == 1:
			child = children[0]
			objType = cmds.objectType(child)
		else:
			objType = cmds.objectType(obj) 
		
		'''print objType'''

		if objType == "mesh":
			suffix = "geo"
		elif objType == "joint":
			suffix = "jnt"
		elif objType == "vamera"
			print "skipping camera"
			continue
		else:
			suffix = "group"

		newName = shortName + "_" + suffix
		cmds.rename(obj, newName)

