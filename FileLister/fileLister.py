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
    addressBar = cmds.textField("AddressBar", w=280, text = startDirectory)
    backButton = cmds.button(label = "<=", w=20, h=20, command = back)
    scrollLayout = cmds.scrollLayout("ContentList", w=200, h=300, hst=0)
    
    # Attach the UI elements to the layout 
    cmds.formLayout(form, edit=True, af=[(addressBar, "top", 10), (addressBar, "left", 30)])
    cmds.formLayout(form, edit = True, af=[(backButton, "top", 10), (addressBar, "left", 10)])
    cmds.formLayout(form, edit=True, af=[(scrollLayout, "top", 40), (scrollLayout, "left", 10)])
    
    # Show window
    cmds.showWindow(window)
    getContents(startDirectory)
        
def back(*args):
    currentPath = cmds.textField("AddressBar", q = True, text = True)
    parentPath = currentPath.rpartition("/")[0].rpartition("/")[0]
    
    if os.path.isdir(parentPath):
        cmds.textField("AddressBar", edit = True, text = parentPath + "/")
        
        # Remove all contents from the list
        cmds.textScrollList("ContentList", edit = True, removeAll = True)
        getContents(parentPath)

def forward(*args):
    currentPath = cmds.textField("AddressBar", q = True, text = True)
    selectedItem = cmds.textScrollList("ContentList", q = True, selectItem = True)[0]
    forwardPath = currentPath + selectedItem + "/"
    
    if os.path.isdir(forwardPath):
        cmds.textField("AddressBar", edit = True, text = forwardPath)
        
        # Remove all contents from the list
        cmds.textScrollList("ContentList", edit = True, removeAll = True)
        getContents(forwardPath)    

def getContents(path):
    fileFilters = ["mb", "ma", "fbx", "obj", "bmp", "jpg", "tga"]
    contents = os.listdir(path)
    validItems = []
    directories = []
    
    for item in contents:
        extension = item.rpartition(".")[2]
        if extension in fileFilters:
            validItems.append(item)
        
        if os.path.isdir(os.path.join(path, item)):
            directories.append(item)
        
    for item in validItems:
        createEntry(item, None)
    
    for item in directories:
        createEntry(item, "menuIconFile.png")
        
def createEntry(item, icon):
    # Create a rowColumnLayout with 2 columns, create an image for the icon, create a button with the label
    layout = cmds.rowColumnLayout(w=200, nc=2)
    if icon != None:
        icon = cmds.iconTextButton(image = icon, w = 30, h = 30)
        button = cmds.button(label = item, w = 150, h = 30)
    else:
        extension = item.rpartition(".")[2]
        icon = cmds.iconTextButton(style = "textOnly", label = extension, w = 20)
        button = cmds.button(label = item, w = 150, h = 30)
         