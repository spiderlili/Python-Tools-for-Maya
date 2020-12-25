def makeStep():
	""" makes a default step """
	import maya.cmds as mc

	# turns the construction history on: the corresponding node will be inserted into the history chain for the mesh
	step, stepHistory = mc.polyCube(name = "step", ch = 1)

	# set height y
	mc.setAttr(stepHistory + ".h", 0.5)

	# set depth z
	mc.setAttr(stepHistory + ".depth", 5.0)

makeStep()