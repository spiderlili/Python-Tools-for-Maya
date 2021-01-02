import sys
sys.path

def sayHello():
	print("Hello!")
sayHello()

def makeStep():
	""" makes a step """
	import maya.cmds as mc
	step,stepHist = mc.polyCube(name = "step", ch = 1)
	mc.setAttr(stepHist + ".h", 0.5)
	mc.setAttr(stepHist + ".depth", 5.0)

makeStep()
