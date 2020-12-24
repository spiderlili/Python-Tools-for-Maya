import maya.cmds as mc

for x in range(0, 20):
	# generate 20 cubes with history
	cube, cubeHistory = mc.polyCube(n = "step" + str(x))

	#offset translation X - equal spacing of 5
	mc.setAttr(cube + ".tx", 2 * x)
	mc.setAttr(cube + ".ty", x)