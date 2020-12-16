import maya.cmds as mc

myCube = mc.polyCube(w = 5, h = 2, d = 0.5, sx = 10, sy = 6, sz = 2, ax = (0,1,0), cuv = 4, ch = 1)
myCube2 = mc.polyCube(name = "jingBox", w = 5, h = 2, d = 0.5, sx = 10, sy = 6, sz = 2, ax = (0,1,0), cuv = 4, ch = False)
print(type(myCube2))
myCube3 = mc.polyCube(name = 'standardCube')

# Convert Mel to Python: relative, objectSpace, worldSpaceDistance (can use short name & long name) - move cube object
# select -r pCube1 ;
# move -r -os -wd 0 0 5 ;
mc.move(5,0,0, myCube3[0], r = True, os = True, wd = True)
mc.rotate(45,10,5, myCube3[0], a = True)