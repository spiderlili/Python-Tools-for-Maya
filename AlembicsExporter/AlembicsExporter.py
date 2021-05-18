import maya.cmds as cmds

def exportAbcMesh(scene, isStaticMesh=True):
	"""
	Export Alembics mesh from specified maya scene, with isStaticMesh boolean to control whether to export 1 single frame or animation with full frame range 
	"""
	if os.path.isfile(scene):
		cmds.file(scene, open=True, force=True)

		meshes = cmds.listRelatives(cmds.ls(type='mesh', v=True), p=True, fullPath=True)
		cmds.select(meshes)

		# string which returns the long root path to the mesh name
		abcStr = ''
		for obj in cmds.ls(sl=True, l=True):
			abcStr += ' -root ' + obj

		cmds.loadPlugin("AbcExport.so")

		if isStaticMesh:
			# export static mesh: 1 single frame
			start, end = 1,1
		else:
			# export mesh animation: min & max time of the frame range
			start, end = cmds.playbackOptions(q=True, minTime=True), cmds.playbackOptions(q=True, maxTime=True) 

		# swap the maya file for abc
		exportPath = scene.replace('.ma', '.abc')
		abcStr = '%s -frameRange %s %s -uvWrite -file %s' % (abcStr, start, end, exportPath)
		cmds.AbcExport(j = abcStr)
		return exportPath