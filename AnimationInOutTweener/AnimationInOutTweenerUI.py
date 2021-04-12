from maya import cmds

def tween(percentage, obj = None, attr = None, selection = True):
	if not obj and not selection:
		raise ValueError("No object is assigned to tween!")