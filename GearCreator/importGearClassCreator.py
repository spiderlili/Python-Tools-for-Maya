import gearClassCreator as gearCreator
reload(gearCreator)

gear = gearCreator.Gear() # create the class
gear.createGear()

print gear.transform