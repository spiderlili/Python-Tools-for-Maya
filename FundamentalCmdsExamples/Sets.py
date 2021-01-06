setList = ['cat',1,2,3,4,5,6,4,3,6,7,'dog']

# get unique values from the list using set command in alphabetical & numerical order
print(set(setList))

setA = {1,2,3,4,5,6}
setB = {3,4,5,6,7,8}

# combine sets using command method or | operator method
print(setA.union(setB))
print(setA | setB)

# see where the sets intersect using command method or & operator method
print(setA.intersection(setB))
print(setA & setB)

# see where the sets differ using command method
print(setA.difference(setB))

# sets are mutable & therefore unhashable. below code will return an error:
# print({1,2,3, {6,7,8}})

# BUT frozen sets are immutable & therefore hashable:
setFrozen = frozenset([6,7,8])
print(setFrozen)

# hash into all the contents of the frozen set & gives back an unique item:
print(hash(setFrozen))