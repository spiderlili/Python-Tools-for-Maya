import maya.cmds as cmds

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
            
addPrefixOrSuffix("prefix")       
