import maya.cmds as cmds
from functools import partial

# TOOD - Prevent error: cannot rename a read only node
def addPrefixOrSuffix(type):
    selection = cmds.ls(sl = True)
    if len(selection) > 0:
        cmds.promptDialog(t = "Add Prefix/Suffix", m = "Enter Name: ", button = ["OK", "Cancel"], db = "OK", cb = "Cancel", dismissString = "Cancel")
        text = cmds.promptDialog(q = True, text = True)
        
        if text != "":
            if type == "prefix":
                for object in selection:
                    cmds.rename(object, text + "_" + object) 
            if type == "suffix":
                for object in selection:
                    cmds.rename(object, object + "_" + text) 
        
    else:
        cmds.confirmDialog(t = "Error", m = "No object selected! Please select at least 1 object.", button = ["OK"], cb = "OK", dismissString = "OK")
            
# addPrefixOrSuffix("prefix")       

def checkBoxChanged(type, *args):
    # Get the value of the passed in checkbox
    # print (args)
    checkboxValue = cmds.checkBox(type + "CheckBox", q = True, v = True)
    if checkboxValue == True:
        cmds.textField(type + "TextField", edit = True, enable = True)
    if checkboxValue == False:
        cmds.textField(type + "TextField", edit = True, enable = False)
        

def accept(*args):
    prefix = cmds.textField("prefixTextField", q = True, text = True)
    suffix = cmds.textField("suffixTextField", q = True, text = True)
    print (prefix)
    print (suffix)

def cancel(*args):
    cmds.deleteUI("renamerUI")

def UI():
    if cmds.window("renamerUI", exists = True):
        cmds.deleteUI("renamerUI")
    window = cmds.window("renamerUI", w = 300, h = 150, title = "Renamer", mxb = False, sizeable = False)
    
    # Create the layout
    layout = cmds.formLayout()
    
    # Create prefix & suffix checkboxes
    prefixCheckBox = cmds.checkBox("prefixCheckBox", label = "Add Prefix", v = False, cc = partial(checkBoxChanged, "prefix"))
    suffixCheckBox = cmds.checkBox("suffixCheckBox", label = "Add Suffix", v = False, cc = partial(checkBoxChanged, "suffix"))
    prefixLabel = cmds.text(label = "Prefix: ")
    prefixText = cmds.textField("prefixTextField", w = 200, enable = False)
    suffixLabel = cmds.text(label = "Suffix: ")
    suffixText = cmds.textField("suffixTextField", w = 200, enable = False)
    
    acceptButton = cmds.button(label = "Accept", w = 130, command = accept)
    cancelButton = cmds.button(label = "Cancel", w = 130, command = cancel)
    
    # Layout the items
    cmds.formLayout(layout, edit = True, af = [(prefixCheckBox, "left", 10), (prefixCheckBox, "top", 10)])
    cmds.formLayout(layout, edit = True, af = [(suffixCheckBox, "left", 100), (suffixCheckBox, "top", 10)])
    cmds.formLayout(layout, edit = True, af = [(prefixText, "left", 50), (prefixText, "top", 40)])
    cmds.formLayout(layout, edit = True, af = [(suffixText, "left", 50), (suffixText, "top", 70)])
    cmds.formLayout(layout, edit = True, af = [(prefixLabel, "left", 10), (prefixLabel, "top", 40)])
    cmds.formLayout(layout, edit = True, af = [(suffixLabel, "left", 10), (suffixLabel, "top", 70)])
    
    cmds.formLayout(layout, edit = True, af = [(acceptButton, "left", 10), (acceptButton, "bottom", 10)])
    cmds.formLayout(layout, edit = True, af = [(cancelButton, "left", 150), (cancelButton, "bottom", 10)])
    
    cmds.showWindow(window)
