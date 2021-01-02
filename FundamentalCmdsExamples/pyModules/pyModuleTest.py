""" module file test: run import sys sys.path.append('moduleFolderPath'), then run import moduleName """

import sys
sys.path

def sayHello():
	print("Hello!")

def makeStep():
	""" makes a step """
	import maya.cmds as mc
	step,stepHist = mc.polyCube(name = "step", ch = 1)
	mc.setAttr(stepHist + ".h", 0.5)
	mc.setAttr(stepHist + ".depth", 5.0)
