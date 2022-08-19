import maya.cmds as cmds
from functools import partial

# TOOD - Prevent error: cannot rename a read only node
def addPrefixOrSuffix(type, text):
    selection = cmds.ls(sl = True)
    if len(selection) > 0:
        # cmds.promptDialog(t = "Add Prefix/Suffix", m = "Enter Name: ", button = ["OK", "Cancel"], db = "OK", cb = "Cancel", dismissString = "Cancel")
        # text = cmds.promptDialog(q = True, text = True)
        
        if text != "":
            if type == "prefix":
                for object in selection:
                    cmds.rename(object, text + "_" + object) 
            if type == "suffix":
                for object in selection:
                    cmds.rename(object, object + "_" + text) 
        
    else:
        cmds.confirmDialog(t = "Error", m = "No object selected! Please select at least 1 object.", button = ["OK"], cb = "OK", dismissString = "OK")

def checkBoxChanged(type, *args):
    # Get the value of the passed in checkbox
    # print (args)
    checkboxValue = cmds.checkBox(type + "CheckBox", q = True, v = True)
    
    if checkboxValue == True:
        if type == "searchReplace":
            cmds.textField("searchTextField", edit = True, enable = True)
            cmds.textField("replaceTextField", edit = True, enable = True)
        else:
            cmds.textField(type + "TextField", edit = True, enable = True)
                    
    if checkboxValue == False:
        if type == "searchReplace":
            cmds.textField("searchTextField", edit = True, enable = False)
            cmds.textField("replaceTextField", edit = True, enable = False)
        else:
            cmds.textField(type + "TextField", edit = True, enable = False)
        
def accept(*args):
    # Get the values of the checkboxes
    prefixCheckBox = cmds.checkBox("prefixCheckBox", q = True, v = True)
    suffixCheckBox = cmds.checkBox("suffixCheckBox", q = True, v = True)
    searchReplaceCheckBox = cmds.checkBox("searchReplaceCheckBox", q = True, v = True)
    
    if prefixCheckBox:
        prefixText = cmds.textField("prefixTextField", q = True, text = True)
        addPrefixOrSuffix("prefix", prefixText)
        cmds.textField("prefixTextField", edit = True, text = "", enable = False) # Clean blank UI after execution
        
    if suffixCheckBox:
        suffixText = cmds.textField("suffixTextField", q = True, text = True)
        addPrefixOrSuffix("suffix", suffixText)
        cmds.textField("suffixTextField", edit = True, text = "", enable = False) # Clean blank UI after execution
    
    if searchReplaceCheckBox:
        searchText = cmds.textField("searchTextField", q = True, text = True)
        replaceText = cmds.textField("replaceTextField", q = True, text = True)
        searchAndReplace(searchText, replaceText)
        
        # Clean blank UI after execution
        searchText = cmds.textField("searchTextField", edit = True, text = "", enable = False)
        replaceText = cmds.textField("replaceTextField", edit = True, text = "", enable = False)
        
    for checkbox in ["prefixCheckBox", "suffixCheckBox", "searchReplaceCheckBox"]:
        cmds.checkBox(checkbox, edit = True, v = False)
    
def searchAndReplace(searchText, replaceText):
    selection = cmds.ls(sl = True)
    notFound = False
    
    if len(selection) > 0:
        for obj in selection:
            if obj.find(searchText) != -1:
                newName = obj.replace(searchText, replaceText)
                cmds.rename(obj, newName)
            if obj.find(searchText) == -1:
                notFound = True
                
    if notFound:
        cmds.confirmDialog(message = "Search text is invalid: did not find anything with '%s'!" %searchText)

def cancel(*args):
    cmds.deleteUI("renamerUI")

def UI():
    if cmds.window("renamerUI", exists = True):
        cmds.deleteUI("renamerUI")
    window = cmds.window("renamerUI", w = 300, h = 200, title = "Renamer", mxb = False, sizeable = False)
    
    # Create the layout
    layout = cmds.formLayout()
    
    # Create prefix & suffix checkboxes
    prefixCheckBox = cmds.checkBox("prefixCheckBox", label = "Add Prefix", v = False, cc = partial(checkBoxChanged, "prefix"))
    suffixCheckBox = cmds.checkBox("suffixCheckBox", label = "Add Suffix", v = False, cc = partial(checkBoxChanged, "suffix"))
    searchReplaceCheckBox = cmds.checkBox("searchReplaceCheckBox", label = "Search / Replace", v = False, cc = partial(checkBoxChanged, "searchReplace"))
    
    prefixLabel = cmds.text(label = "Prefix: ")
    prefixText = cmds.textField("prefixTextField", w = 200, enable = False)
    suffixLabel = cmds.text(label = "Suffix: ")
    suffixText = cmds.textField("suffixTextField", w = 200, enable = False)
    
    searchLabel = cmds.text(label = "Search For: ")
    searchText = cmds.textField("searchTextField", w = 200, enable = False)
    replaceLabel = cmds.text(label = "Replace With: ")
    replaceText = cmds.textField("replaceTextField", w = 200, enable = False)
    
    acceptButton = cmds.button(label = "Accept", w = 130, command = accept)
    cancelButton = cmds.button(label = "Cancel", w = 130, command = cancel)
    
    # Layout the items
    cmds.formLayout(layout, edit = True, af = [(prefixCheckBox, "left", 10), (prefixCheckBox, "top", 10)])
    cmds.formLayout(layout, edit = True, af = [(suffixCheckBox, "left", 100), (suffixCheckBox, "top", 10)])
    cmds.formLayout(layout, edit = True, af = [(searchReplaceCheckBox, "right", 10), (searchReplaceCheckBox, "top", 10)])
    cmds.formLayout(layout, edit = True, af = [(prefixText, "left", 50), (prefixText, "top", 30)])
    cmds.formLayout(layout, edit = True, af = [(suffixText, "left", 50), (suffixText, "top", 60)])
    cmds.formLayout(layout, edit = True, af = [(prefixLabel, "left", 10), (prefixLabel, "top", 30)])
    cmds.formLayout(layout, edit = True, af = [(suffixLabel, "left", 10), (suffixLabel, "top", 60)])

    cmds.formLayout(layout, edit = True, af = [(searchText, "left", 80), (searchText, "top", 100)])
    cmds.formLayout(layout, edit = True, af = [(replaceText, "left", 80), (replaceText, "top", 120)])
    cmds.formLayout(layout, edit = True, af = [(searchLabel, "left", 10), (searchLabel, "top", 100)])
    cmds.formLayout(layout, edit = True, af = [(replaceLabel, "left", 10), (replaceLabel, "top", 120)])
    
    cmds.formLayout(layout, edit = True, af = [(acceptButton, "left", 10), (acceptButton, "bottom", 10)])
    cmds.formLayout(layout, edit = True, af = [(cancelButton, "left", 150), (cancelButton, "bottom", 10)])
    
    cmds.showWindow(window)
