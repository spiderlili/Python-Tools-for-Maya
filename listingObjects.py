from maya import cmds
selection = print cmds.ls(selection = True)

if len(selection) == 0: #get a new selection
	selection = cmds.ls(dag = True, long = True) 

#sort using the length of the objects because children will have a longer full name: act on them first to not affect their path
selection.Sort(key = len, reverse = True) 
print selection