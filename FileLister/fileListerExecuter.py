# TODO: copy code to userSetup.py to auto-run this script everytime the user starts Maya
import maya.cmds as cmds
import os, sys
import importlib

fileListerPath = "/Users/jingtan/Dropbox (Tripledot)/My Mac (Jings-MacBook-Pro.local)/Documents/GitHub/Python-Tools-for-Maya/FileLister"
# sys.path.remove(fileListerPath)
sys.path.append(fileListerPath)

doesSysPathExist = os.path.exists(fileListerPath)
print(sys.path)

def launchCustomFileLister():
    import fileLister 
    importlib.reload(fileLister)
    fileLister.UI()
    
# if doesSysPathExist == False:
# sys.path.append(fileListerPath)

launchCustomFileLister()

scriptJobNum = cmds.scriptJob(event = ["NewSceneOpened", launchCustomFileLister])