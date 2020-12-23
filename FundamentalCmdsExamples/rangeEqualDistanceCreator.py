import maya.cmds as mc

myCube = mc.polyCube(n = 'MyCube')[0]

# set translation in relative & world space
mc.xform(myCube, ws = True, t = (5,5,5))
mc.xform(myCube, r = True, t = (5,5,5))

# get translation in relative & world space using query
mc.xform(myCube, ws = True, t = True, q = True)

# set rotation relative and os space in euler angles, may cause gimbal rotation issues when using euler angles & 2 axis are on top of each other
mc.xform(myCube, eu = True, ro = (45,45,45))
mc.xform(myCube, r = True, eu = True, ro = (45,90,120))
mc.xform(myCube, ws = True, eu = True, ro = (45,45,45))

# gimbal lock: same visible rotation but matrix values differ
mc.xform(myCube, ws = True, eu = True, ro = (45,90,120))
mc.xform(myCube, eu = True, ro = (45,90,120))

# get rotation
mc.xform(myCube, ws = True, ro = True, q = True)

import pymel.core as pm
pos1 = pm.selected()[0].getMatrix()

# no visible differences in matrices but not the same
mc.xform(myCube, ws = True, eu = True, ro = (45, 90, 120))
mc.xform(myCube, eu = True, ro = (45, 90, 120))