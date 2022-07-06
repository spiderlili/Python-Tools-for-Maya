import maya.cmds as cmds
import os

def UI():
    # Check to see if window exists
    if cmds.window("customFileLister",exists=True):
        cmds.deleteUI("customFileLister")
    
    # Create window
    window = cmds.window("customFileLister", w=300, h=400, sizeable = False, mnb=True, mxb=True, title="File Lister")
    
    # Create window layout
    form = cmds.formLayout(w=300, h=400)
    
    # Create address bar
    startDirectory = cmds.internalVar(uwd = True) # Default to project directory
    addressBar = cmds.textField("Address Bar", w=280, text = startDirectory)
    contentList = cmds.textScrollList("ContentList", w=200, h=300, ams=False)
    
    # Attach the UI elements to the layout
    cmds.formLayout(form, edit=True, af=[(addressBar, "top", 10), (addressBar, "left", 10)])
    cmds.formLayout(form, edit=True, af=[(contentList, "top", 40), (contentList, "left", 10)])
    
    # Show window
    cmds.showWindow(window)
    getContents(startDirectory)
    
    
def getContents(path):
    contents = os.listdir(path)
    for item in contents:
        cmds.textScrollList("ContentList", edit = True, append = item)
    