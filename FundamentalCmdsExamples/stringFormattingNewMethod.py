# .format() versions: python 2.7 or above
import os

# get username from operating environment in upper case
username = os.getenv("USERNAME").upper()

print("my name is: {0}" .format(username))

# more than value using tuple
firstName = "Alice"
lastName = "Liddell"

print("Alice in Wonderland: {0} {1}".format(firstName, lastName))

# can reverse order: unable to do this with the old formatting expressions %s
print("Alice in Wonderland: {1} {0}".format(firstName, lastName))

# more than value using dictionary (keyname), unpack the dictionary
aliceName = {'firstName': 'Alice', 'lastName':'Liddell'}
print("Alice in Wonderland:{firstName} {lastName}".format(**aliceName))

# string formatting for numbers (float to int) - d as decimal points to create ints
import random
randomFloat = random.random() * 100

# d will not work due to no forced coercion in .format(), need to cast randomFloat to int or use 0 precision float for int 
print("random float as int: {:d}".format(int(randomFloat)))
print("random float as int: {:.0f}".format(randomFloat))

# float has 6 decimal points precision by default but can be changed:
print("random float as default float: {f}".format(randomFloat))
print("random float as truncated 2 decimal points float: {.2f}".format(randomFloat))
print("random float as float with 10 positions including the decimal and 2 after point: {010.2f}".format(randomFloat))
print("random float as an exponent: {.2e}".format(randomFloat))

# with precision of 12 decimals: new method vs old method - can add padding (8 in this case)
print("random float as float with 10 positions including the decimal and 2 after point: %0.12f" %randomFloat)
print("random float as float with 10 positions including the decimal and 2 after point: {0:8:12f}".format(randomFloat))

#left justify with trailing values to fill the zone of 20, fill the trailing values with @
print("random float as float with 10 positions including the decimal and 2 after point: {0:<20:12f}".format(randomFloat))
print("random float as float with 10 positions including the decimal and 2 after point: {0:@<20:12f}".format(randomFloat))
print("random float as float with 10 positions including the decimal and 2 after point: {0:@>20:12f}".format(randomFloat))

# exponent left justified and filling with 0s for 20 chars, switch to exponent E if the  number is too large
print("random float as float with 10 positions including the decimal and 2 after point: {0:-020.3g}".format(randomFloat))