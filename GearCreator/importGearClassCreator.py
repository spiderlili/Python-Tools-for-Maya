import gearClassCreator as gearCreator
reload(gearCreator)

gear = gearCreator.Gear() # create the class
gear.createGear()
gear.changeTeeth(teeth=10, length=0.1)

print gear.transform
print type(gear)