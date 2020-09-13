import maya.cmds as cmds

class Gear(object):
    def createGear(self, teeth=10, length = 0.3):
        spans = teeth * 2
        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis = spans)
        sideFaces = range(spans * 2, spans * 3, 2)

        cmds.select(clear=True)
        for face in sideFaces:
            cmds.select('%s.f[%s]' %(self.transform, face), add = True)

        self.extrudeFaces = cmds.polyExtrudeFacet(localTranslateZ=length)[0]

    def changeTeeth(self, constructor, extrudeFaces, teeth=10, length=0.3):
        spans = teeth * 2
        # use polypipe with the poly pipe that you already have. use edit flag so it knows to edit the existing one instead of creating a new one
        cmds.polyPipe(constructor, edit=True, subdivisionsAxis=spans)
        sideFaces = range(spans * 2, spans * 3, 2)
        faceNames = []

        for face in sideFaces:
            faceName = 'f[%s]' % (face)
            faceNames.append(faceName)

        # print faceNames
        # get the length of the faceNames list, give it to setAttr(), get list of all the faces to use: expand the face names list so each one will be a parameter
        cmds.setAttr('%s.inputComponents' % (extrudeFaces), len(faceNames), *faceNames, type="componentList")
        cmds.polyExtrudeFacet(extrudeFaces, edit=True, ltz=length)  # localTranslateZ shorthand
