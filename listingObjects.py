from maya import cmds
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
	print shortName
	children = cmds.listRelatives()