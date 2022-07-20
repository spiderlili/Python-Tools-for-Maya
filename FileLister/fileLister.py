import maya.cmds as cmds
import os
from functools import partial

def UI():
    # Check to see if window exists
    if cmds.window("customFileLister",exists=True):
        cmds.deleteUI("customFileLister")
    
    # Create window
    window = cmds.window("customFileLister", w=300, h=400, sizeable = False, mnb=True, mxb=True, title="File Lister")
    
    # Create window layout
    form = cmds.formLayout(w=300, h=400)
    
    # Create address bar widgets
    startDirectory = cmds.internalVar(uwd = True) # Default to project directory
    addressBar = cmds.textField("AddressBar", w=280, text = startDirectory, parent = form)
    backButton = cmds.button(label = "<=", w=30, h=20, command = back, parent = form)
    fileFilters = cmds.optionMenu("FileFiltersOptionMenu", label = "", w = 80, parent = form, cc = partial(getContents, None)) # changeCommand
    searchField = cmds.textField("searchTextField", w=90, text = "search")
    scrollLayout = cmds.scrollLayout("ContentList", w=200, h=300, hst=0)
    
    # Add menuItems to the optionMenu dropdown
    for item in ["All Files", "Maya Files", "Import Files", "Textures"]:
        cmds.menuItem(label = item, parent = fileFilters)
    
    # Attach the UI elements to the layout 
    cmds.formLayout(form, edit=True, af=[(addressBar, "top", 10), (addressBar, "left", 30)])
    cmds.formLayout(form, edit = True, af=[(backButton, "top", 10), (addressBar, "left", 10)])
    cmds.formLayout(form, edit=True, af=[(scrollLayout, "top", 40), (scrollLayout, "left", 10)])
    cmds.formLayout(form, edit=True, af=[(fileFilters, "top", 40), (fileFilters, "right", 10)])
    cmds.formLayout(form, edit=True, af=[(searchField, "top", 70), (searchField, "right", 0)])
    
    # Show window
    cmds.showWindow(window)
    getContents(startDirectory)
        
def back(*args):
    currentPath = cmds.textField("AddressBar", q = True, text = True)
    parentPath = currentPath.rpartition("/")[0].rpartition("/")[0]
    
    if os.path.isdir(parentPath):
        cmds.textField("AddressBar", edit = True, text = parentPath + "/")

        getContents(parentPath)

def forward(item, *args):
    currentPath = cmds.textField("AddressBar", q = True, text = True)
    forwardPath = currentPath + item + "/"
    
    if os.path.isdir(forwardPath):
        cmds.textField("AddressBar", edit = True, text = forwardPath)
        
        getContents(forwardPath)

# Use *args when being called from UI
def getContents(path, *args): 
    if path == None:
        path = cmds.textField("AddressBar", q = True, text = True)
    
    # Remove all contents from the list if there are children
    children = cmds.scrollLayout("ContentList", q = True, childArray = True)
    # print (children)
    if children != None:        
        for child in children:
           cmds.deleteUI(child)
           
    allFileFilters = ["mb", "ma", "fbx", "obj", "bmp", "jpg", "tga", "png"]
    mayaFiles = ["mb", "ma"]
    importFiles = ["obj", "fbx"]
    textureFiles = ["bmp", "jpg", "tga", "png"]
    fileFilters = []
    
    # Look up current filter selection in the option menu
    currentFilter = cmds.optionMenu("FileFiltersOptionMenu", q = True, v = True)
    if currentFilter == "All Files":
        fileFilters = allFileFilters
    if currentFilter == "Maya Files":
        fileFilters = mayaFiles
    if currentFilter == "Import Files":
        fileFilters = importFiles
    if currentFilter == "Textures":
        fileFilters = textureFiles
    
    contents = os.listdir(path)
    validItems = []
    directories = []
    
    for item in contents:
        extension = item.rpartition(".")[2]
        if extension in fileFilters:
            validItems.append(item)
        
        if os.path.isdir(os.path.join(path, item)):
            directories.append(item)

    for item in directories:
        createEntry(item, "menuIconFile.png")
            
    for item in validItems:
        createEntry(item, None)
                
def createEntry(item, icon):
    # Create a rowColumnLayout with 2 columns, create an image for the icon, create a button with the label
    layout = cmds.rowColumnLayout(w=200, nc=2, parent = "ContentList") 
    
    if icon != None:
        icon = cmds.iconTextButton(command = partial(forward, item), parent=layout, image=icon, w=190, h=20, style = "iconAndTextHorizontal", label=item)
    else:
        icon = cmds.iconTextButton(command = partial(forward, item), parent=layout, w=190, h=20, style = "iconAndTextHorizontal", label=item)

         