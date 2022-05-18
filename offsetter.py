def toAbsolute(listofpairlist, listofsizes):
	for sizeindex in range(1, len(listofsizes)):
		# Convert sequential sizes to cumulative.
		listofsizes[sizeindex] += listofsizes[sizeindex-1]
	
	for vi in range(1, len(listofpairlist)):
		# Add size of previous section to the relative offset.
		for pair in listofpairlist[vi]:
			pair[0] += listofsizes[vi-1]
	
	returnlist = []
	for l in range(len(listofpairlist)):
		returnlist += listofpairlist[l]
	
	return returnlist

def swapEndianness(hexstring):
	ba = bytearray.fromhex(hexstring)
	ba.reverse()
	return ba.hex()