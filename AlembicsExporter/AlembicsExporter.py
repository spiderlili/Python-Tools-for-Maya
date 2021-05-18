import maya.cmds as cmds

def exportMesh(scene):
	"""
	Export mesh
	"""
	if os.path.isfile(scene):
		cmds.file(scene, open=True, force=True)

		meshes = cmds.listRelatives(cmds.ls(type='mesh', v=True), p=True, fullPath=True)
		cmds.select(meshes)

		abcStr = ''
		for obj in cmds.ls(sl=True, l=True):
			abcStr += '-root ' + obj

		cmds.loadPlugin("AbcExport.so")
		start,end = 1,1

		export = scene.replace('.ma', '.abc')
		abcStr = '%s -frameRange %s %s -uvWrite -file %s' % (abcStr, start, end, export)
		cmds.AbcExport(j = abcStr)
		return export