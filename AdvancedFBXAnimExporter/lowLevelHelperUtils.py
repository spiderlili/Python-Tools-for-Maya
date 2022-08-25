import maya.cmds as cmds
import maya.mel # TODO: find equivalents of fbx export options in python
import string

# Set the root hierarchy attribute. Tag the given node with the origin attribute & set to true. 
# If the object exists & the attribute does not exist, add the attribute & set to true.
def TagForOrigin(node):
   if cmds.objExists(node) and not cmds.objExists(node + ".origin"):
        cmds.addAttr(node, shortName = "org", longName = "origin", at = "bool")
        cmds.setAttr(node + ".origin", True)
        
TagForOrigin("locator1")        
TagForOrigin("pCone1")        