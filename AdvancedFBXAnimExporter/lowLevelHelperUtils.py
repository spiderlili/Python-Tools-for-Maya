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
        
# Return the origin of the given namespace. 
# If namespace is not empty string: list all joints with the matching namespace, else list all joints        
# Assumes namespace & origin attribute is on a joint. For list of joints, look for origin attribute & check if it's set to true. If found, return joint name. 
def ReturnOrigin(namespace):
    joints = []
    if namespace:
        joints = cmds.ls((namespace + ":*"), type = "joint") # namespace must NOT include colon:
    else:
        joints = cmds.ls(type = "joint")
    
    if len(joints):
        for joint in joints:
            if cmds.objExists(joint + ".origin") and cmds.getAttr(joint + ".origin"):
                print (joint)
                return joint
                
    print("Error: No joint with .origin attribute on is found!")
    return "Error: No joint with .origin attribute on is found!"
   
# Tests
# TagForOrigin("joint1")
# ReturnOrigin("")