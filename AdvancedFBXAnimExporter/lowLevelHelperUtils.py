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
            if cmds.objExists(joint + ".origin") and cmds.getAttr(joint + ".origin"): # .origin must be ON
                print (joint)
                return joint
                
    print("Error: No joint with .origin attribute on is found!")
    return "Error: No joint with .origin attribute on is found!"

# Return the meshes connected to blend shape nodes (the rest are not needed by animation exports),
# Get a list of blend shape nodes & follow those connections to the mesh shape node, traverse up the hierarchy to find the parent transform node
# The character must have a valid namespace & the namespace must NOT have ":" colon. Only supports single layer referencing & polygonal meshes (not NURBS)
def FindMeshWithBlendShapes(namespace):
    returnArray = []
    blendshapes = cmds.ls((namespace + ":*"), type = "blendShape")
    for blendshape in blendshapes:
        downstreamNodes = cmds.listHistory(blendshape, future = True)
        for node in downstreamNodes:
            if cmds.objectType(node, isType = "mesh"):
                parents = cmds.listRelatives(node, parent = True)
                returnArray.append(parents[0]) # Only has 1 parent on each instance
    if len(returnArray) == 0:
        print("No blend shapes are found!")
        return
    return returnArray
    
# Remove all nodes tagged as garbage, list all transforms in the scene
# Use deleteMe attribute to mark the attribute signifying garbage
def ClearGarbage():
    list = cmds.ls(tr = True)
    for obj in list:
        if cmds.objExists(obj + ".deleteMe"):
            cmds.delete(obj)

# Tag object for being garbage. If node is valid object & attribute does not exist, add deleteMe attribute
def TagForGarbage(node):
    if cmds.objExists(node) and not cmds.objExists(node + ".deleteMe"):
        cmds.addAttr(node, shortName = "del", longName = "deleteMe", at = "bool")
        cmds.setAttr(node + ".deleteMe", True)
        
# Delete given export node: if object exists, delete node
def DeleteFBXExportNode(exportNode):
    if cmds.objExists(exportNode):
        cmds.delete()
    return

# Add the attribute to the export node to store export settings
# For each attribute you want to add: check if it exists & add if it doesn't exist
# Assume fbxExport node is a valid object
def AddFBXNodeAttrs(fbxExportNode):
    return

# Tests
# TagForGarbage("pCube1")
# ClearGarbage()
# TagForOrigin("joint1")
# ReturnOrigin("")
# FindMeshWithBlendShapes("")    