from maya import cmds

def tween(percentage, obj = None, attrs = None, selection = True):
	# if obj is not given & selection is set to false: error
	if not obj and not selection:
		raise ValueError("No object is assigned to tween!")

	# if no obj is specified: get it from the 1st selection
	if not obj:
		obj = cmds.ls(selection = True)[0]

	# query the object from selection & list all keyable attributes
	if not attrs:
		attrs = cmds.listAttr(obj, keyable = True)

	currentTime = cmds.currentTime(query = True)

	for attr in attrs:
		# construct the full name of the attribute with its object - many maya cmds require this format
		attrFull = '%s.%s' % (obj, attr) 

		# get the keyframes of the attribute on this object
		keyframes = cmds.keyframe(attrFull, query = True)

		if not keyframes:
			continue

		previousKeyframes = []
		for frame in keyframes:
			if frame < currentTime: # it's a previous keyframe
				previousKeyframes.append(frame)

		# list comprehension: same as above previousKeyframes forloop 
		laterKeyframes = [frame for frame in keyframes if frame > currentTime]

		# safe check to prevent errors before continuing onto the next item in the list
		if not previousKeyframes and not keyframes:
			continue

		# figure out whichever the closest previous frame is
		if previousKeyframes: 
			previousFrame = max(previousKeyframes)
		else:
			previousFrame = None

		# shorthand: same as above previousKeyframes logic
		nextFrame = min(laterKeyframes) if laterKeyframes else None

		# query the attribute at the given time
		previousFrameValue = cmds.getAttr(attrFull, time = previousFrame)
		nextFrameValue = cmds.getAttr(attrFull, time = nextFrame)

		print previousFrameValue, nextFrameValue

		# Calculate the amount needed to add on to the previous value to get the current value 
		frameValueDifference = nextFrameValue - previousFrameValue
		weightedValueDifference = (frameValueDifference * percentage) / 100.0
		currentValue = previousFrameValue + weightedValueDifference
		print currentValue
		
		cmds.setKeyframe(attrFull, time = currentTime, value = currentValue)

tween(50)