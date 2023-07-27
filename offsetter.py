def toAbsolute(template, sizes):
	for sizeindex in range(1, len(sizes)):
		# Convert sequential sizes to cumulative.
		sizes[sizeindex] += sizes[sizeindex-1]
	
	for vi in range(1, len(template)):
		# Add size of previous section to the relative offset.
		for pair in template[vi]:
			pair[0] += sizes[vi-1]
	
	returnlist = []
	for l in range(len(template)):
		returnlist += template[l]
	
	return returnlist

def swapEndianness(hexstring):
	ba = bytearray.fromhex(hexstring)
	ba.reverse()
	return ba.hex()