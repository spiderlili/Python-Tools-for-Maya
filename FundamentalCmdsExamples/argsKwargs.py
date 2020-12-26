import maya.cmds as mc

def numbers(*args):
    print(args)
    for arg in args:
        print("arg = " + str(arg))
        
tupleTest = (3,5,6,789)
listTest = [3,5,6,789]
numbers(*listTest)

def names(**kwargs):
	print(kwargs)
	# get each item tuple in dictionary
	for k,v in kwargs.items():
		print("key = " + k)
		print("value = " + v)

names(Superman = "Clark Kent", Batman = "Bruce Wayne", Spiderman = "Peter Parker")