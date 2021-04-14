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

# UI window using cmds: inherit from object
class TweenWindow(object):
	windowName = "Tweener Window" # static - will not change no matter what
	def show(self):
		if cmds.window(self.windowName, query = True, exists = True): #delete window if it already exists
			cmds.deleteUI(self.windowName)

		cmds.window(windowName)
		self.buildUI()
		cmds.showWindow()

	def buildUI(self):
		column = cmds.columnLayout()
		cmds.text(label = "Use this slider to set the tween amount")

		# whenever the slider has changed: will call the tween command. without parenthesis() => run the function rather than execute it immediately
		row = cmds.rowLayout(numberOfColumns = 2)
		self.slider = cmds.floatSlider(min = 0, max = 100, value = 50, step = 1, changeCommand = tween)

		cmds.button(label = "Reset", command = self.reset)

		# Maya commands stores the last layout it created: anything you make after that gets added to that layout. set parent to column to avoid layout issues
		cmds.setParent(column)
		cmds.button(label = "Close", command = self.close)

	def reset(self, *args): # maya button sends 1 extra value to any function they're calling. everything not specified in this function will be stored in args
		cmds.floatSlider(self.slider, edit = True, value = 50) # reset to default value of 50

	def close(self, *args):
		cmds.deleteUI(self.windowName)

tween(50)
tween.TweenWindow.show()