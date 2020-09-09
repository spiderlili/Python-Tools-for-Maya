import maya.cmds as cmds
import random

def assignRandomColorToID():
    materialSelection = cmds.ls(mat = True)
    for material in materialSelection:
        cmds.vray("addAttributesFromGroup", material, "vray_material_id", 1)
        randomColour = [random.random() for i in range(3)]
        cmds.setAttr('%s.vrayColorId' % material, randomColour[0], randomColour[1], randomColour[2], type='double3')

assignRandomColorToID()
