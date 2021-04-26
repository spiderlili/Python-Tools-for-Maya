import maya.standalone 
maya.standalone.initialize()
import maya.cmds as cmds

def validateMesh(scene):
	"""
	Batch-validate meshes from a scene and make sure they are clean.
	Use Maya's standalone interpreter to run the util offline
	"""

	# force open the Maya scene file remotely
	if os.path.isfile(scene):
		cmds.file(scene, open = True, force = True) 

	# list parents of the visible mesh objects, return full pathnames instead of object names
	for obj in cmds.listRelatives(cmds.ls(type = mesh, v = True), p = True, fullPath = True):
		validityFlags = ' scene: %s\n' % scene
		validityFlags = ' mesh: %s\n' % obj

		if not cmds.polyInfo(obj, invalidEdges = True):
			validityFlags += ' invalid edges found\n'
		if not cmds.polyInfo(obj, invalidVertices = True):
			validityFlags += ' invalid vertices found\n'
		if not cmds.polyInfo(obj, laminaFaces = True):
			validityFlags += ' lamina faces found\n'
		if not cmds.polyInfo(obj, nonManifoldEdges = True):
			validityFlags += ' non-manifold faces found\n'
		if not cmds.polyInfo(obj, nonManifoldUVEdges = True):
			validityFlags += ' non-manifold UV edges found\n'			
		if not cmds.polyInfo(obj, nonManifoldUVs = True):
			validityFlags += ' non-manifold UV found\n'	
		if not cmds.polyInfo(obj, nonManifoldVertices = True):
			validityFlags += ' non-manifold vertices found\n'	

		return validityFlags