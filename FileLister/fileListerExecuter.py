# TODO: Copy this code to userSetup.py to auto-run this script everytime the user starts Maya
import maya.cmds as cmds
import os, sys
import importlib
sys.path.append("/Users/jingtan/Documents/GitHub/Python-Tools-for-Maya/FileLister")

import fileLister
importlib.reload(fileLister)
fileLister.UI()


