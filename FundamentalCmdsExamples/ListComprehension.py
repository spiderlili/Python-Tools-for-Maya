oddsList = []

# traditional way: for loop
for x in range(0, 50):
	if x % 2:
		oddsList.append(x)

# list comprehension: faster than for loop under the hood
oddListComprehension = [x for x in range(0,50) if x % 2]