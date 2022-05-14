from colors import *

def colorBytes(view, data, col, pos, howmany):
	# Function to insert color markup in final string.
	if view == 0:
		pos = (pos-1)*3
		data = data[:pos] + col + data[pos:]
		# To seek past "[color=xxxxxx]".
		pos += 14
		# To seek past the bytes to be colored.
		howmany = howmany*3
		for seek in range(howmany):
			pos += 1
		data = data[:pos] + cc + data[pos:]
	else:
		# 81, 4
		pos = (pos-1)*2
		data = data[:pos] + col + data[pos:]
		# To seek past "[color=xxxxxx]".
		pos+=14
		howmany = howmany*2
		for seek in range(howmany):
			pos += 1
		data = data[:pos] + cc + data[pos:]
	# print(data)
	return data