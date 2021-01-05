import os

# get username from operating environment in upper case
username = os.getenv("USERNAME").upper()

print("my name is: %s" % username)

# more than value using tuple
firstName = "Alice"
lastName = "Liddell"

print("Alice in Wonderland: %s %s" %(firstName, lastName))

# more than value using dictionary (keyname)
aliceName = {'firstName': 'Alice', 'lastName':'Liddell'}
print("Alice in Wonderland: %(firstName)s %(lastName)s" %aliceName)

# string formatting for numbers (float to int) using %i or %d
import random
randomFloat = random.random() * 100
print("random float as int: %i" %randomFloat)

# float has 6 decimal points precision by default but can be changed:
print("random float as default float: %f" %randomFloat)
print("random float as truncated 2 decimal points float: %.2f" %randomFloat)
print("random float as float with 10 positions including the decimal and 2 after point: %010.2f" %randomFloat)
print("random float as an exponent: %.2e" % randomFloat)