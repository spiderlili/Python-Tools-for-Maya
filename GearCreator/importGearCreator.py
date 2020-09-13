import gearCreator
# refresh the code in maya
reload(gearCreator)

# constructor, transform, extrudeFaces = gearCreator.createGear()
gearCreator.changeTeeth(constructor, extrude, teeth = 40)

# get documentation
help(gearCreator.createGear)