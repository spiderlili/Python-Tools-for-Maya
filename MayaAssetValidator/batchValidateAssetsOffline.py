import os
import osUtils
import AssetValidatorStandalone

# write asset validation results to textfile
def main(assetDir):
	fileObj = open(os.path.join(assetDir, 'report.txt'), 'a')
	scenes = osUtils.getFilesOfType(assetDir, 'ma') # find maya files
	for scene in scenes:
		validateResults = AssetValidatorStandalone.validateMesh(scene)
		print validateResults

		fileObj.write(validate)
	fileObj.close() 

# import data from main(assetDir) into another tool without running main(), make sure to only run main when running this script without import
if __name__ == '__main__':
	main(sys.argv[-1]) # pass in the asset directory, get the second argument which is passed in
