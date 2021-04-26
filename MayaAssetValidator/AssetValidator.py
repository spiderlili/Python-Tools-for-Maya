import maya.cmds as cmds

def validateMesh():
	"""
	Validate the mesh and make sure it's clean
	"""

	# list parents of the visible mesh objects, return full pathnames instead of object names
	for obj in cmds.listRelatives(cmds.ls(type = mesh, v = True), p = True, fullPath = True):
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