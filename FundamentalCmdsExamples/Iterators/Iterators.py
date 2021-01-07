# use r to prevent certain letters in the directory being misread as unicode when combined with '\'
frankenstein = open(r'D:\github\Python-Tools-for-Maya\FundamentalCmdsExamples\Iterators\Frankenstein.txt')

# bad way to open & close: must close file at the end, inefficient & slow
# print(frankenstein.readline())
# print(frankenstein.next())
# frankenstein.close()

# better way to open & close: with command: for loop converts object to iterable, calling next() under the hood
# frankensteinList = iter(frankenstein)
for x in frankenstein:
	print(x)

string = "Jing"
iterStr = iter(string)
for x in iterStr:
	print(x)

frankenstein.close()