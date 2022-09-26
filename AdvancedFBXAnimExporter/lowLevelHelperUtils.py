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
def FindMeshesWithBlendShapes(namespace):
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
        cmds.delete(exportNode)

# Add the attribute to the export node to store export settings
# For each attribute you want to add: check if it exists & add if it doesn't exist
# Assume fbxExport node is a valid object
def AddFBXNodeAttrs(fbxExportNode):
    if not cmds.attributeQuery("export", node = fbxExportNode, exists = True):
        cmds.addAttr(fbxExportNode, longName = 'export', at = "bool")
    
    if not cmds.attributeQuery("moveToOrigin", node = fbxExportNode, exists = True):
        cmds.addAttr(fbxExportNode, longName = 'moveToOrigin', at = "bool")
        
    if not cmds.attributeQuery("zeroOrigin", node = fbxExportNode, exists = True): # Kill all anims on origin
        cmds.addAttr(fbxExportNode, longName = 'zeroOrigin', at = "bool")
        
    if not cmds.attributeQuery("exportName", node = fbxExportNode, exists = True): 
        cmds.addAttr(fbxExportNode, longName = 'exportName', dt = "string")   
    
    if not cmds.attributeQuery("useSubRange", node = fbxExportNode, exists = True): 
        cmds.addAttr(fbxExportNode, longName = 'useSubRange', at = "bool")   

    if not cmds.attributeQuery("startFrame", node = fbxExportNode, exists = True): 
        cmds.addAttr(fbxExportNode, longName = 'startFrame', at = "float")   
        
    if not cmds.attributeQuery("endFrame", node = fbxExportNode, exists = True): 
        cmds.addAttr(fbxExportNode, longName = 'endFrame', at = "float")   
         
    if not cmds.attributeQuery("exportMeshes", node = fbxExportNode, exists = True): 
        cmds.addAttr(fbxExportNode, longName = 'exportMeshes', at = "message")            
            
    if not cmds.attributeQuery("exportNode", node = fbxExportNode, exists = True): 
        cmds.addAttr(fbxExportNode, shortName = "xnd", longName = 'exportNode', at = "message")    
    
    if not cmds.attributeQuery("animLayers", node = fbxExportNode, exists = True): 
        cmds.addAttr(fbxExportNode, longName = 'animLayers', dt = "string")   

# Create the export node to store export settings, create an empty transform node
# Send it to AddFBXNodeAttrs to add the needed export attributes
def CreateFBXExportNode(characterName):
    fbxExportNode = cmds.group(em = True, name = characterName + "FBXExportNode#")
    AddFBXNodeAttrs(fbxExportNode)
    cmds.setAttr(fbxExportNode + ".export", 1)
    return fbxExportNode

# Return all export nodes connected to the given origin. 
# If origin is valid & has the exportNode attribute: return list of export nodes connected to it.
# Assumes that only export nodes are connected to the exportNode attribute.
def ReturnFBXExportNodes(origin):
    exportNodeList = []
    if cmds.objExists(origin + ".exportNode"):
        exportNodeList = cmds.listConnections(origin + ".exportNode")

    return exportNodeList

# Connect the FBX Export node to the origin. 
# Check if attribute exist & nodes are valid: if they are, connect attributes
def ConnectFBXExportNodeToOrigin(exportNode, origin):
    if cmds.objExists(origin) and cmds.objExists(exportNode): 
        if not cmds.objExists(origin + ".exportNode"):
            TagForExportNode(origin)
        if not cmds.objExists(exportNode + ".exportNode"):
            AddFBXNodeAttrs(fbxExportNode)
        
        cmds.connectAttr(origin + ".exportNode", exportNode + ".exportNode")

# Model Export Procedures
# Connect the meshes to the export node so the exporter can find them. Assumes that meshes is a list of transform nodes for polygon meshes 
# check to make sure meshes & exportNode is valid, check for attribute "exportMeshes". If no attribute, add it & then connect attributes. 
def ConnectFBXExportNodeToMeshes(exportNode, meshes):
    if cmds.objExists(exportNode):
        if not cmds.objExists(exportNode + ".exportMeshes"):
            AddFBXNodeAttrs(fbxExportNode)
            
    for mesh in meshes:
        if cmds.objExists(mesh):
            if not cmds.objExists(exportNode + ".exportMeshes"):
                TagForMeshExport(mesh)
            cmds.connectAttr(exportNode + ".exportMeshes", mesh + ".exportMeshes", force = True)

# Disconnect the message attribute between export node & mesh. 
# Iterate through list of meshes. If mesh exists: disconnect. Assumes the node & mesh are connected via exportMeshes message attribute.     
def DisconnectFBXExportNodeToMeshes(exportNode, meshes):
    if cmds.objExists(exportNode):
        for mesh in meshes:
            if cmds.objExists(mesh):
                cmds.disconnectAttr(exportNode + ".exportMeshes", mesh + ".exportMeshes")

# Return a list of meshes connected to the export node. 
# List connections to exportMeshes attribute. assumes exportMeshes is valid - exportMeshes attribute is used to connect to the export meshes. 
def ReturnConnectedMeshes(exportNode):
    meshes = cmds.listConnections((exportNode + ".exportMeshes"), source = False, destination = True)
    return meshes

# Animation Export Procedures

def UnlockJointTransforms(root):
    hierarchy = cmds.listRelatives(root, ad = True, f = True)
    hierarchy.append(root) # Add root joint to the list
    
    for child in hierarchy:
        cmds.setAttr((child + '.translateX'), lock = False)
        cmds.setAttr((child + '.translateY'), lock = False)
        cmds.setAttr((child + '.translateZ'), lock = False)
        cmds.setAttr((child + '.rotateX'), lock = False)
        cmds.setAttr((child + '.rotateY'), lock = False)
        cmds.setAttr((child + '.rotateZ'), lock = False)
        cmds.setAttr((child + '.scaleX'), lock = False)
        cmds.setAttr((child + '.scaleY'), lock = False)
        cmds.setAttr((child + '.scaleZ'), lock = False)

# Connect 1 node to another by connecting given node to the other given node via specified transform. 
# 2 given nodes must exist & transform type (translate / rotate / scale) must be valid.
def ConnectAttrs(sourceNode, destNode, transform):
    cmds.connectAttr(sourceNode + "." + transform + "X",  destNode + "." + transform + "X")
    cmds.connectAttr(sourceNode + "." + transform + "Y",  destNode + "." + transform + "Y")
    cmds.connectAttr(sourceNode + "." + transform + "Z",  destNode + "." + transform + "Z")
 
# Copy the bind skeleton, connect the copy to the original bind skeleton
# Duplicate hierarchy, delete everything that's not a joint.
# Unlock all the joints in the copy in order to make connections without errors.
# Connect the translates, rotates, scales. Parent copy to the world for clean exporrt. Add deleteMe attr to get rid of the copy when export is done
def CopyAndConnectSkeleton(origin):
    newHierarchy = []
    if origin != "Error" and cmds.objExists(origin):
        duplicateHierarchy = cmds.duplicate(origin)
        tempHierarchy = cmds.listRelatives(duplicateHierarchy[0], ad = True, f = True)
        
        for child in tempHierarchy:
            if cmds.objExists(child):
                if cmds.objectType(child) != "joint":
                    cmds.delete(child)
        
        UnlockJointTransforms(duplicateHierarchy[0]) 
        originalHierarchy = cmds.listRelatives(origin, ad = True, type = "joint")
        newHierarchy = cmds.listRelatives(duplicateHierarchy[0], ad = True, type = "joint")
        originalHierarchy.append(origin)
        newHierarchy.append(duplicateHierarchy[0])
        
        for index in range(len(originalHierarchy)):
            ConnectAttrs(originalHierarchy[index], newHierarchy[index], "translate")
            ConnectAttrs(originalHierarchy[index], newHierarchy[index], "rotate")
            ConnectAttrs(originalHierarchy[index], newHierarchy[index], "scale")

        cmds.parent(duplicateHierarchy[0], world = True)
        TagForGarbage(duplicateHierarchy[0])
    
    return newHierarchy

# Translate export skeleton to origin, may or may not kill origin animation depending on input 
# Bake the animation onto the duplicate skeleton's origin 
# Create an anim layer which will either be additive or override depending on input parameters. 
# Add deleteMe attribute to animLayer => when exoprt is done, it will remove the animLayer.   
def TransformToOrigin(origin, startFrame, endFrame, zeroOrigin):
    cmds.bakeResults(origin, t = (startFrame, endFrame), at = ["rx", "ry", "rz", "tx", "ty", "tz", "sx", "sy", "sz"], hi = "none")
    cmds.select(clear = True)
    cmds.select(origin)
    newAnimLayer = ""
    
    # Override layer: kill all animations on the origin
    if zeroOrigin:
        newAnimLayer = cmds.animLayer(aso = True, mute = False, solo = False, override = True, passthrough = True, lock = False) 
        cmds.setAttr(newAnimLayer + ".rotationAccumulationMode", 0)
        cmds.setAttr(newAnimLayer + ".scaleAccumulationMode", 0)
    else: # Additive: shifts origin animations
        newAnimLayer = cmds.animLayer(aso = True, mute = False, solo = False, override = False, passthrough = False, lock = False) 
    
    TagForGarbage(newAnimLayer)
    
    # Turn anim layer on 
    cmds.animLayer(newAnimLayer, edit = True, weight = 1)
    cmds.setKeyframe(newAnimLayer + ".weight")
    
    # Move origin animation to world origin
    cmds.setAttr(origin + ".translate", 0, 0, 0)
    cmds.setAttr(origin + ".rotate", 0, 0, 0)
    cmds.setKeyframe(origin, al = newAnimLayer, t = startFrame)
 
# Animation Layer Procedures
# Record the animLayer settings used in animation & store in the exportNode as a string. List all anim layers, query their mute & solo attributes
# Use ; as sentinal value to split separate anim layers. 
# Use , as sentinal value to split separate fields for animLayer. 
# Use = as sentinal value to split separate attributes from their values in field. 

def SetAnimLayerSettings(exportNode):
    if not cmds.attributeQuery("animLayers", node = exportNode, exists = True): 
        AddFBXNodeAttrs(exportNode)
        
    animLayers = cmds.ls(type = "animLayer")
    animLayerCommandStr = ""
    for layer in animLayers:
        mute = cmds.animLayer(layer, query = True, mute = True)
        solo = cmds.animLayer(layer, query = True, solo = True)
        animLayerCommandStr += (layer + ", mute = " + str(mute) + ", solo = " + str(solo) + ";")
    
    cmds.setAttr(exportNode + ".animLayers", animLayerCommandStr, type = "string")

# Set the animlayers based on the string value in the exportNode. Use pre-defined sentinal values to split the string for separate animLayers. 
# Parse out the attributes & their values, then set according to order: layer, mute, solo
    
def SetAnimLayersFromSettings(exportNode):
    if cmds.objExists(exportNode) and not cmds.objExists(node + ".animLayers"):
        animLayersRootString = cmds.getAttr(exportNode + ".animLayers", asString = "True")
    
        if animLayersRootString:
            animLayerEntries = animLayersRootString.split(";")
            
            for entry in animLayerEntries:
                if entry:
                    fields = entry.split(",")
                    animLayerField = fields[0]
                    muteField = fields[1]
                    soloField = fields[2]
                    
                    muteFieldStr = muteField.split(" = ")
                    soloFieldStr = soloField.split(" = ")
                    
                    # Convert strings to bool values
                    muteFieldBool = True
                    soloFieldBool = True
                    if muteFieldStr[1] != "True":
                        muteFieldBool = False
                    
                    if soloFieldStr[1] != "True":
                        soloFieldBool = False
                    
                    cmds.animLayer(animLayerField, edit = True, mute = muteFieldBool, solo = soloFieldBool)
    
def ClearAnimLayerSettings(exportNode):
    cmds.setAttr(exportNode + ".animLayers", "", type = "string")

# Export Procedures
def ExportFBXAnimation(characterName, exportNode):
    ClearGarbage()
    characters = []
    
    if characterName:
        characters.append(characterName)
    else:
        reference = cmds.file(reference = 1, query = True)
        for currentReference in references:
            characers.append(cmds.file(currentReference, namespace = 1, query = True))
    
    for character in characters:
        # Get meshes with blend shapes
        meshes = FindMeshesWithBlendShapes(character)
        
        # Get origin
        origin = ReturnOrigin(character)
        
        exportNodes = []
        
        if exportNode:
            exportNodes.append(exportNode)
        else:
            exportNodes = ReturnFBXExportNodes(origin)
        
        for currentExportNode in exportNodes:
            if cmds.getAttr(currentExportNode + ".export") and origin != "Error": # Check if export is turned on
                exportRig = CopyAndConnectSkeleton(origin) # Create dummy skeleton
        
def ExportFBXCharacter(exportNode):
    return
    
# Called by procs in FBXAnimationModelExportOptions.mel
def ExportFBX(exportNode): 
    currentProjectWorkspace = cmds.workspace(q = True, rd = True) # Will fail if absolute path. Look up the value of root directory
    fileName = cmds.getAttr(exportNode + ".exportName")
    if fileName:
        newFBX = currentProjectWorkspace + fileName
        cmds.file(newFBX, force = True, type = 'FBX export', pr = True, es = True)
    else:
        cmds.warning("No Valid Export Filename for Export Node: " + exportNode + "\n")

# Tests
# UnlockJointTransforms("joint1")
# ConnectAttrs("joint1", "joint5", "rotate")
# CreateFBXExportNode("test")
# AddFBXNodeAttrs("group1")
# TagForGarbage("pCube1")
# ClearGarbage()
# TagForOrigin("pCube1")
# TagForOrigin("joint1")
# ReturnOrigin("")
# FindMeshesWithBlendShapes("")    