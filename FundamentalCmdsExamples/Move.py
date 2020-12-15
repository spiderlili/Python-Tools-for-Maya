import maya.cmds as mc

# Convert Mel to Python: relative, objectSpace, worldSpaceDistance (can use short name & long name) - move cube object
# select -r pCube1 ;
# move -r -os -wd 0 0 5 ;

mc.move(5,0,0, 'pCube1', r = True, os = True, wd = True)
