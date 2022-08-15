import maya.cmds as cmds

# TOOD - Prevent error: cannot rename a read only node
def addSuffix():
    selection = cmds.ls(sl = True)
    if len(selection) > 0:
        cmds.promptDialog(t = "Add Suffix", m = "Enter Suffix Name: ", button = ["OK", "Cancel"], db = "OK", cb = "Cancel", dismissString = "Cancel")
        suffixText = cmds.promptDialog(q = True, text = True)
        if suffixText != "":
            for object in selection:
                cmds.rename(object, object + "_"+ suffixText) 
    else:
        cmds.promptDialog(t = "Error", m = "No object selected! Please select at least 1 object.")
            
addSuffix()       
