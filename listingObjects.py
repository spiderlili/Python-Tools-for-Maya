from maya import cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "ambientLight": "lgt",
    "camera": None
}

DEFAULT_SUFFIX = "grp"


def rename(selection=False):
    """
    This function will rename any objects to have the correct suffix
    Args:
        selection: whether or not to use the current selection
    Returns:
        a list of all the objects we operated on
    """
    objects = cmds.ls(selection=selection, dag=True, long=True)

	if selection and not objects:
		raise RuntimeError("You don't have anything selected")
	'''sort using the length of the objects because children will have a longer full name: act on them first to not affect their path'''
	objects.sort(key=len, reverse=True)

    '''sort using length of the objects as children will have a longer full name: act on them 1st to not affect their path '''
    for obj in objects:
        short_name = obj.split("|")[-1]
        '''print shortName'''
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []
        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        '''print objType'''

        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)
        if not suffix:
            continue

        if obj.endswith('_' + suffix):
            continue

        new_name = "%s_%s" % (short_name, suffix)
        cmds.rename(obj, new_name)

		index = objects.index(obj)
		objects[index] = obj.replace(short_name, new_name)
	return objects
