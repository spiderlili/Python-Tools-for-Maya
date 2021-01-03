import maya.cmds as mc

# without closures
def makeAcube(x):
	# avoid 0
	inc = str(x + 1)
	cube = mc.polyCube(name = "cube" + inc)
	return cube

def cubeStack(numCubes = 10):
	""" Makes a stack of cubes """
	for x in range(numCubes):
		cube = makeAcube(x)
		# set the name of the transform to assemble the value for the translateY attribute, raise its height
		mc.setAttr(cube[0] + ".ty", (x *1) + 0.5)

# with closures: no longer have the makeACube function taking up memory & able to get the value of x because it's a child of the function
def cubesStack(numCubes = 10):
	""" Makes a stack of cubes """
	def makeAcube():
		# avoid 0
		inc = str(x + 1)
		cube = mc.polyCube(name = "cube" + inc)
		return cube

	for x in range(numCubes):
		cube = makeAcube()
		# set the name of the transform to assemble the value for the translateY attribute, raise its height
		mc.setAttr(cube[0] + ".ty", (x *1) + 0.5)


cubesStack()


