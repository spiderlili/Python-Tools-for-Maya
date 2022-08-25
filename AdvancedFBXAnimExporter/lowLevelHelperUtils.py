import maya.cmds as cmds
import maya.mel # TODO: find equivalents of fbx export options in python
import string

# Set the root hierarchy attribute. Tag the given node with the origin attribute & set to true. 
# If the object exists & the attribute does not exist, add the attribute & set to true.
def TagForOrigin(node):
   if cmds.objExists(node) and not cmds.objExists(node + ".origin"):
        cmds.addAttr(node, shortName = "org", longName = "origin", at = "bool")
        cmds.setAttr(node + ".origin", True)
        
# Add attributes to the mesh so the exporter can find them
# If the object exists & attribute does not exist: add the exportMeshes message attribute
def TagForMeshExport(mesh):
    if cmds.objExists(mesh) and not cmds.objExists(mesh + ".exportMeshes"):
        cmds.addAttr(mesh, shortName = "xms", longName = "exportMeshes", at = "message")
        
# Add attributes to the node so the exporter can find export definitions
# If the object exists & attribute does not exist: add the exportNode message attribute
def TagForExportNode(node):
    if cmds.objExists(node) and not cmds.objExists(node + ".exportNode"):
        cmds.addAttr(node, shortName = "xnd", longName = "exportNode", at = "message")