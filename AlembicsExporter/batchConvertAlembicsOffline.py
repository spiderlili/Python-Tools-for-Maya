import sys
import os
import osUtils
import AlembicsExporter

# works with mayapy to convert maya scenes (.ma) in a passed asset directory to Alembics meshes (.abc) offline
def main(assetDir):
	scenes = osUtils.getFilesOfType(assetDir, 'ma') # find maya files
	for scene in scenes:
		abc = AlembicsExporter.exportAbcMesh(scene)
		print 'Exported: ', abc

# import data from main(assetDir) into another tool without running main(), make sure to only run main when running this script without import
if __name__ == '__main__':
	main(sys.argv[-1]) # pass in the asset directory, get the second argument which is passed in
