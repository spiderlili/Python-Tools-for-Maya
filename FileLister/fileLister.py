import maya.cmds as cmds
import os
from functools import partial
import pickle

searchFieldDefaultStr = "search"

def defineFileFilterTypes():
    allFileFilters = ["mb", "ma", "fbx", "obj", "bmp", "jpg", "tga", "png"]
    mayaFiles = ["mb", "ma"]
    importFiles = ["obj", "fbx"]
    textureFiles = ["bmp", "jpg", "tga", "png"]

def UI():
    # Check to see if window & dockControl already exists to prevent error
    if cmds.window("customFileLister",exists=True):
        cmds.deleteUI("customFileLister")
    
    if cmds.dockControl("fileListerDock", exists=True):
        cmds.deleteUI("fileListerDock")
    
    # Create window
    window = cmds.window("customFileLister", w=300, h=400, sizeable = False, mnb=True, mxb=True, title="File Lister")
    
    # Create window layout
    form = cmds.formLayout(w=300, h=400)
    
    # Create address bar widgets
    startDirectory = cmds.internalVar(uwd = True) # Default to project directory
    addressBar = cmds.textField("AddressBar", w=280, text = startDirectory, parent = form)
    backButton = cmds.button(label = "<=", w=30, h=20, command = back, parent = form)
    fileFilters = cmds.optionMenu("FileFiltersOptionMenu", label = "", w = 80, parent = form, cc = partial(getContents, None)) # changeCommand
    
    searchField = cmds.textField("searchTextField", w=90, text = searchFieldDefaultStr, cc = partial(getContents, None)) # Figure out path by itself
    
    # Add Favourite folders to a list
    addFavoritesButton = cmds.button(label = "Add Favourite", w=90, c = addFavorite)
    favoriteList = cmds.scrollLayout("FavoriteList", w=90, h=200, parent = form)
    scrollLayout = cmds.scrollLayout("ContentList", w=200, h=300, hst=0, parent = form) # Hide the scrollbar
     
    # Add menuItems to the optionMenu dropdown
    for item in ["All Files", "Maya Files", "Import Files", "Textures"]:
        cmds.menuItem(label = item, parent = fileFilters)
    
    # Attach the UI elements to the layout 
    cmds.formLayout(form, edit=True, af=[(addressBar, "top", 10), (addressBar, "left", 30)])
    cmds.formLayout(form, edit = True, af=[(backButton, "top", 10), (addressBar, "left", 10)])
    cmds.formLayout(form, edit=True, af=[(scrollLayout, "top", 40), (scrollLayout, "left", 10)])
    cmds.formLayout(form, edit=True, af=[(fileFilters, "top", 40)], ac = [fileFilters, "left", 5, scrollLayout]) # Attach fileFilters to scrollLayout
    cmds.formLayout(form, edit=True, af=[(searchField, "top", 70)], ac = [searchField, "left", 5, scrollLayout]) # Attach searchField to scrollLayout
    cmds.formLayout(form, edit=True, af=[(addFavoritesButton, "top", 100)], ac=[addFavoritesButton, "left", 5, scrollLayout]) # Attach AddFavouritesButton
    cmds.formLayout(form, edit=True, af=[(favoriteList, "top", 130)], ac=[favoriteList, "left", 5, scrollLayout])
    
    # Show dock control, allow all areas for docking
    cmds.dockControl("fileListerDock", area = "left", content = window, w = 310, aa = "all")
   
    # Show window
    #cmds.showWindow(window)
    getContents(startDirectory)
    loadFavorites()
        
def back(*args):
    currentPath = cmds.textField("AddressBar", q = True, text = True)
    parentPath = currentPath.rpartition("/")[0].rpartition("/")[0] + "/"
    
    if os.path.isdir(parentPath):
        cmds.textField("AddressBar", edit = True, text = parentPath + "/")
        getContents(parentPath)

def forward(item, *args):
    currentPath = cmds.textField("AddressBar", q = True, text = True)
    forwardPath = currentPath + item + "/"
    print (currentPath)
    print (forwardPath)
    
    if os.path.isdir(forwardPath):
        cmds.textField("AddressBar", edit = True, text = forwardPath)
        getContents(forwardPath)
    else:
        # TODO: Remove repetition of file filters code, condense into 1 reusable function. 
        allFileFilters = ["mb", "ma", "fbx", "obj", "bmp", "jpg", "tga", "png"]
        mayaFiles = ["mb", "ma"]
        importFiles = ["obj", "fbx"]
        textureFiles = ["bmp", "jpg", "tga", "png"]
        
        # Check for Maya files
        fileExtension = item.rpartition(".")[2]
        if fileExtension in mayaFiles:
            result = cmds.confirmDialog(title = "File Operation", button = ["Open", "Import", "Reference", "Cancel"], cancelButton = "Cancel", dismissString = "Cancel")
        
            if result == "Open":
                cmds.file(currentPath + item, open = True, force = True)
                
            if result == "Import":
                cmds.file(currentPath + item, i = True, force = True)
                
            if result == "Reference":
                # Reference the file into a namespace with the same name as item file name without the extension
                cmds.file(currentPath + item, r = True, loadReferenceDepth = "all", namespace = item.rpartition(".")[0])
        
        # Check for Import files
        if fileExtension in importFiles:
            result = cmds.confirmDialog(title = "File Operation", button = ["Import", "Cancel"], cancelButton = "Cancel", dismissString = "Cancel")
            if result == "Import":
                cmds.file(currentPath + item, i = True, force = True)

        # Check for Texture files, create a material & assign to each selected object 
        if fileExtension in textureFiles:
            result = cmds.confirmDialog(title = "File Operation", button = ["Assign To Selected Objects", "Cancel"], cancelButton = "Cancel", dismissString = "Cancel")
            if result == "Assign To Selected Objects":
                selection = cmds.ls(sl = True) 
                if len(selection) > 0:
                    material = cmds.shadingNode("phong", asShader = True, name = item.rpartition(".")[0] + "_Mat")
                    place2DTexNode = cmds.shadingNode("place2dTexture", asUtility = True)
                    textureFile = currentPath + item
                    texture = cmds.shadingNode("file", asTexture = True)
                    cmds.connectAttr(place2DTexNode + ".outUV", texture + ".uvCoord")
                    cmds.connectAttr(texture + ".outColor", material + ".color")
                    cmds.setAttr(texture + ".fileTextureName", textureFile, type = "string")
                                
                    for obj in selection:
                        cmds.select(obj)
                        cmds.hyperShade(assign = material)
                        cmds.select(clear = True)
                        

def addFavorite(*args):
    currentPath = cmds.textField("AddressBar", q = True, text = True)
    niceName = currentPath.rpartition("/")[0].rpartition("/")[2]
    createEntry(niceName, "menuIconFile.png", "FavoriteList", currentPath, True)
    
    # Create favorites.txt in the user prefs directory: /Users/jingtan/Library/Preferences/Autodesk/maya/2022/prefs 
    favoritesFilePath = cmds.internalVar(upd = True) + "favorites.txt" 
    favoritesFile = open(favoritesFilePath, 'wb') # w = write mode, wb = write binary mode
    
    children = cmds.scrollLayout("FavoriteList", q = True, childArray = True)
    buttons = []
    for child in children:
        button = cmds.rowColumnLayout(child, q = True, childArray = True)[0] # Return icon text button
        buttons.append(button)
    
    favorites = []
    for button in buttons:
        annotation = cmds.iconTextButton(button, q = True, ann = True)
        favorites.append(annotation)
    
    pickle.dump(favorites, favoritesFile)
    favoritesFile.close()

# Use *args when being called from UI. Update the folder path text field if the user pass in a path (when it's a favorite) 
def getContents(path, *args): 
    if path == None:
        path = cmds.textField("AddressBar", q = True, text = True)
    else: # This is causing issues - can't go forward when clicking on folder
        cmds.textField("AddressBar", edit = True, text = path)
    
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
        createEntry(item, "menuIconFile.png", "ContentList", "")
        
    # Search file filter
    searchString = cmds.textField("searchTextField", q = True, text = True)
    if searchString != searchFieldDefaultStr or "":            
        for item in validItems:
            if item.find(searchString) != -1:
                createEntry(item, None, "ContentList", "")
    else:
        for item in validItems:
            createEntry(item, None, "ContentList", "")
      
def loadFavorites():
    favoritesFilePath = cmds.internalVar(upd = True) + "favorites.txt" 
    if os.path.exists(favoritesFilePath):
        favoritesFile = open(favoritesFilePath, 'rb') # r = Read-only, rb = read bites
        favorites = pickle.load(favoritesFile)
        
        for favorite in favorites:
            niceName = favorite.rpartition("/")[0].rpartition("/")[2]
            createEntry(niceName, "menuIconFile.png", "FavoriteList", favorite, True)
            # print (favorite)
        
        favoritesFile.close()

def createEntry(item, icon, scrollLayout, annotationStr, isFavorite = False):
    # Create a rowColumnLayout with 2 columns, create an image for the icon, create a button with the label. annotationStr is the full folder path
    layout = cmds.rowColumnLayout(w=200, nc=2, parent = scrollLayout) 
    
    if isFavorite == False:
        if icon != None:
            icon = cmds.iconTextButton(command = partial(forward, item), parent=layout, image=icon, w=190, h=20, style = "iconAndTextHorizontal", label=item, ann = annotationStr)
        else:
            icon = cmds.iconTextButton(command = partial(forward, item), parent=layout, w=190, h=20, style = "iconAndTextHorizontal", label=item, ann = annotationStr)
    else:
        icon = cmds.iconTextButton(command = partial(getContents, annotationStr), parent=layout, image=icon, w=190, h=20, style = "iconAndTextHorizontal", label=item, ann = annotationStr)
