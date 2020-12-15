import maya.cmds as mc

# Convert Mel to Python
# move -r -os -wd 0 0 5 ;

mc.move(r = True, os = True, wd =(5,0,0) )
