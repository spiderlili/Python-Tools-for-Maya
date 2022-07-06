import maya.cmds as cmds
import os

def UI():
    # Check to see if window exists
    if cmds.window("customFileLister",exists=True):
        cmds.deleteUI("customFileLister")
    
    # Create window
    window = cmds.window("customFileLister", w=300, h=600, mnb=True, mxb=True, title="File Lister")
    
    # Show window
    cmds.showWindow(window)