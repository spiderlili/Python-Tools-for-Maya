import maya.cmds as cmds

# default settings for good use case
def createGear(teeth = 10, length = 0.3):
    """
    create a gear with the specified parameters:
    Args:
        teeth: the number of teeth to create
        length: the length of teeth

    Returns:
        a tuple of the constructor, transform, polyExtrude node
    """
    # teeth are every alternate face = spans * 2
    spans = teeth * 2
    transform, constructor = cmds.polyPipe(subdivisionsAxis = spans)

    sideFaces = range(spans * 2, spans * 3, 2)
    cmds.select(clear = True)
    for face in sideFaces:
        cmds.select('%s.f[%s]' %(transform, face), add = True)

    # extrude faces, set its Z local translation vector to be the same as specified length in function call
    extrudeFaces = cmds.polyExtrudeFacet(localTranslateZ = length)[0]

    # gives back useful data to manipulate the gear: tuple of transform node, constructor & polyExtrudeFace
    return constructor, transform, extrudeFaces

def changeTeeth(constructor, extrudeFaces, teeth = 10, length = 0.3):
    spans = teeth * 2
    # use polypipe with the poly pipe that you already have. use edit flag so it knows to edit the existing one instead of creating a new one
    cmds.polyPipe(constructor, edit = True, subdivisionsAxis = spans)
    sideFaces = range(spans * 2, spans * 3, 2)
    faceNames = []

    for face in sideFaces:
        faceName = 'f[%s]' % (face)
        faceNames.append(faceName)

    # print faceNames
    # get the length of the faceNames list, give it to setAttr(), get list of all the faces to use: expand the face names list so each one will be a parameter
    cmds.setAttr('%s.inputComponents' %(extrudeFaces), len(faceNames), *faceNames, type = "componentList")
    cmds.polyExtrudeFacet(extrudeFaces, edit = True, ltz = length) # localTranslateZ shorthand

constructor, transform, extrudeFaces = createGear()
changeTeeth(constructor, extrudeFaces, teeth = 30, length=1)